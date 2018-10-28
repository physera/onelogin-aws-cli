"""OneLogin/AWS Business logic"""

from typing import Optional

import configparser
import xml.etree.ElementTree as ElementTree

import base64
import boto3
import os
import re

import ipify

from onelogin.api.client import OneLoginClient

from onelogin_aws_cli.configuration import Section
from onelogin_aws_cli.credentials import MFACredentials, UserCredentials
from onelogin_aws_cli.userquery import user_role_prompt

CONFIG_FILENAME = ".onelogin-aws.config"
DEFAULT_CONFIG_PATH = os.path.join(os.path.expanduser("~"), CONFIG_FILENAME)


class OneloginAWS(object):
    """
    Handles the authentication between OneLogin SAML Assertion and the AWS
    identity federation
    """

    def __init__(self, config: Section):
        self.sts_client = boto3.client("sts")
        self.config = config
        self.saml = None
        self.all_roles = None
        self.role_arn = None
        self.credentials = None
        self.duration_seconds = int(config['duration_seconds'])
        self.user_credentials = UserCredentials(config)
        self.mfa = MFACredentials(config)

        base_uri_parts = self.config['base_uri'].split('.')
        self.ol_client = OneLoginClient(
            self.config['client_id'],
            self.config['client_secret'],
            base_uri_parts[1],
        )

    def check_for_errors(self, response):
        """
        Throw exceptions that the OneLogin API should have thrown
        """

        if self.ol_client.error is None:
            return response

        raise Exception("Onelogin Error: '{error}' '{desc}'".format(
            error=self.ol_client.error,
            desc=self.ol_client.error_description
        ))

    def get_saml_assertion(self):
        """
        Retrieve users credentials and get the SAML assertion from Onelogin,
        based on the users choice of AWS account to log into
        """

        self.user_credentials.load_credentials()

        saml_resp = self.check_for_errors(
            self.ol_client.get_saml_assertion(
                username_or_email=self.user_credentials.username,
                password=self.user_credentials.password,
                app_id=self.config['aws_app_id'],
                subdomain=self.config['subdomain'],
                ip_address=self.get_ip_address(),
            )
        )

        if saml_resp.mfa:
            if not self.mfa.ready():
                self.mfa.select_device(saml_resp.mfa.devices)
                if not self.mfa.has_otp:
                    self.mfa.prompt_token()

            saml_resp = self.check_for_errors(
                self.ol_client.get_saml_assertion_verifying(
                    self.config['aws_app_id'],
                    self.mfa.device.id,
                    saml_resp.mfa.state_token,
                    self.mfa.otp
                )
            )

        self.saml = saml_resp

    def get_ip_address(self) -> Optional[str]:
        """
        Get the client IP address.
        Uses either the `ip_address` in config,
        or if `auto_determine_ip_address` is specified in config,
        the ipify service is used to dynamically lookup the IP address.
        """

        # if ip address has been hard coded in config file, use that
        ip_address = self.config.get('ip_address')
        if ip_address is not None:
            return ip_address

        # if auto determine is enabled, use ipify to lookup the ip
        if self.config.auto_determine_ip_address:
            ip_address = ipify.get_ip()
            return ip_address

    def get_arns(self):
        """Extract the IAM Role ARNs from the SAML Assertion"""

        if not self.saml:
            self.get_saml_assertion()
        # Parse the returned assertion and extract the authorized roles
        aws_roles = []
        root = ElementTree.fromstring(
            base64.b64decode(self.saml.saml_response))

        namespace = "{urn:oasis:names:tc:SAML:2.0:assertion}"
        role_name = "https://aws.amazon.com/SAML/Attributes/Role"
        for attr in root.iter(namespace + "Attribute"):
            if attr.get("Name") == role_name:
                for val in attr.iter(namespace + "AttributeValue"):
                    aws_roles.append(val.text)

        # Note the format of the attribute value should be role_arn,
        # principal_arn but lots of blogs list it as principal_arn,role_arn so
        # let's reverse them if needed
        aws_roles = [role.split(",") for role in aws_roles]
        aws_roles = [(role, principal) for role, principal in aws_roles]
        self.all_roles = aws_roles

    def get_role(self):
        """
        Prompt the user to choose a Role ARN if more than one is available
        """

        if not self.all_roles:
            self.get_arns()

        if not self.all_roles:
            raise Exception("No roles found")

        # If I have more than one role, ask the user which one they want,
        # otherwise just proceed

        self.role_arn, self.principal_arn = user_role_prompt(
            self.all_roles,
            saved_choice=self.config.get("role_arn"),
        )

    def assume_role(self):
        """Perform an AWS SAML role assumption"""

        if not self.role_arn:
            self.get_role()
        if self.config['region']:
            self.sts_client = boto3.client(
                "sts",
                region_name=self.config["region"])
        res = self.sts_client.assume_role_with_saml(
            RoleArn=self.role_arn,
            PrincipalArn=self.principal_arn,
            SAMLAssertion=self.saml.saml_response,
            DurationSeconds=self.duration_seconds
        )

        self.credentials = res

    def save_credentials(self):
        """Save the AWS Federation credentials to disk"""

        if not self.credentials:
            self.assume_role()

        creds = self.credentials["Credentials"]

        cred_file = self._initialize_credentials()

        cred_config = configparser.ConfigParser()
        cred_config.read(cred_file)

        # Update with new credentials
        name = self.credentials["AssumedRoleUser"]["Arn"]
        m = re.search(r'(arn\:aws([\w-]*)\:sts\:\:)(.*)', name)

        if m is not None:
            name = m.group(3)
        name = name.replace(":assumed-role", "")
        if "profile" in self.config:
            name = self.config["profile"]

        # Initialize the profile block if it is undefined
        if name not in cred_config:
            cred_config[name] = {}

        # Set each value specifically instead of overwriting the entire
        # profile block in case they have other parameters defined
        cred_config[name]['aws_access_key_id'] = creds["AccessKeyId"]
        cred_config[name]['aws_secret_access_key'] = creds["SecretAccessKey"]
        cred_config[name]['aws_session_token'] = creds["SessionToken"]

        # Set region for this profile if passed in via configuration
        if self.config['region']:
            cred_config[name]['region'] = self.config['region']

        with open(cred_file, "w") as cred_config_file:
            cred_config.write(cred_config_file)

        print("Credentials cached in '{}'".format(cred_file))
        print("Expires at {}".format(creds["Expiration"]))
        print("Use aws cli with --profile " + name)

        # Reset state in the case of another transaction
        self.credentials = None

    def _initialize_credentials(self):
        cred_file = os.environ.get('AWS_SHARED_CREDENTIALS_FILE', None)

        if cred_file is None:
            cred_file = os.path.expanduser("~/.aws/credentials")
            cred_dir = os.path.expanduser("~/.aws/")
            if not os.path.exists(cred_dir):
                os.makedirs(cred_dir)

        return cred_file
