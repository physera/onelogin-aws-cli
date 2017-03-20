#!/usr/bin/env python3

import configparser
import getpass
import json
import os

import requests
import boto3

CONFIG_FILENAME = ".onelogin-aws.config"


def user_choice(question, options):
    print(question + "\n")
    option_list = ""
    for i in range(0, len(options)):
        option_list += ("{}. {}\n".format(i+1, options[i]))
    selection = None
    while not selection:
        print(option_list)
        choice = input("? ")
        try:
            val = int(choice) - 1
            if val in range(0, len(options)):
                selection = options[val]
            else:
                print("Invalid option")
        except ValueError:
            print("Invalid option")
    return selection


class OneloginAWS(object):
    def __init__(self, config):
        self.sts_client = boto3.client("sts")
        self.config = config
        self.token = None
        self.account_id = None
        self.saml = None
        self.credentials = None
        self.user = None

    def request(self, path, headers, data):
        res = requests.post(
            self.config["base_uri"] + path,
            headers=headers,
            data=json.dumps(data)
        )

        if res.status_code == 200:
            if "data" in res.json():
                return res.json()["data"]
            else:
                return res.json()
        else:
            raise Exception("Error: {}".format(res.json()))

    def get_token(self):
        headers = {
            "Authorization": "client_id:{}, client_secret:{}".format(
                self.config["client_id"], self.config["client_secret"]),
            "Content-Type": "application/json"
        }
        data = {"grant_type": "client_credentials"}
        res = self.request("auth/oauth2/token", headers, data)
        self.token = res[0]["access_token"]
        self.account_id = res[0]["account_id"]

    def get_saml_assertion(self):
        if not self.token:
            self.get_token()

        email = input("Onelogin Username: ")
        password = getpass.getpass("Onelogin Password: ")
        params = {
            "app_id": self.config["aws_app_id"],
            "username_or_email": email,
            "password": password,
            "subdomain": self.config["subdomain"]
        }
        headers = {
            "Authorization": "bearer:{}".format(self.token),
            "Content-Type": "application/json"
        }
        res = self.request("api/1/saml_assertion", headers, params)
        callback = res[0]["callback_url"]
        state_token = res[0]["state_token"]
        self.user = res[0]["user"]
        if callback:
            devices = res[0]["devices"]
            device_id = None
            if len(devices) > 1:
                for i in range(0, len(devices)):
                    print("{}. {}".format(i+1, devices[i]["device_type"]))
                device_num = input("Which OTP Device? ")
                device_id = devices[int(device_num)-1]["device_id"]
            else:
                device_id = devices[0]["device_id"]

            otp_token = input("OTP Token: ")

            params = {
                "app_id": self.config["aws_app_id"],
                "device_id": str(device_id),
                "state_token": state_token,
                "otp_token": otp_token
            }
            res = self.request("api/1/saml_assertion/verify_factor",
                               headers, params)
            self.saml = res

    def assume_role(self):
        if not self.saml:
            self.get_saml_assertion()
        res = self.sts_client.assume_role_with_saml(
            RoleArn=self.config["aws_role_arn"],
            PrincipalArn=self.config["aws_principal_arn"],
            SAMLAssertion=self.saml
        )

        self.credentials = res

        headers = {
            "Authorization": "bearer:{}".format(self.token),
            "Content-Type": "application/json"
        }

        self.request("api/1/events", headers, {
            "event_type_id": 8,
            "account_id": self.account_id,
            "user_id": self.user["id"],
            "user_name": "{} {}".format(self.user["firstname"],
                                        self.user["lastname"]),
            "app_id": int(self.config["aws_app_id"]),
        })

    def save_credentials(self):
        if not self.credentials:
            self.assume_role()

        creds = self.credentials["Credentials"]

        cred_file = os.path.expanduser("~/.aws/credentials")
        cred_config = configparser.ConfigParser()
        cred_config.read(cred_file)

        # Update with new credentials
        name = self.credentials["AssumedRoleUser"]["Arn"]
        if name.startswith("arn:aws:sts::"):
            name = name[13:]
        name = name.replace(":assumed-role", "")

        cred_config[name] = {
            "aws_access_key_id": creds["AccessKeyId"],
            "aws_secret_access_key": creds["SecretAccessKey"],
            "aws_session_token": creds["SessionToken"]
        }

        with open(cred_file, "w") as cred_config_file:
            cred_config.write(cred_config_file)

        print("Credentials cached in '{}'".format(cred_file))

    @staticmethod
    def generate_config():
        print("Configure Onelogin and AWS\n\n")
        config = configparser.ConfigParser()
        config.add_section("default")
        default = config["default"]

        default["base_uri"] = user_choice("Pick a Onelogin API server:", [
            "https://api.us.onelogin.com/",
            "https://api.eu.onelogin.com"
        ])

        print("\nOnelogin API credentials. These can be found at:\n"
              "https://admin.us.onelogin.com/api_credentials")
        default["client_id"] = input("Onelogin API Client ID: ")
        default["client_secret"] = input("Onelogin API Client Secret: ")
        print("\nOnelogin AWS App ID. This can be found at:\n"
              "https://admin.us.onelogin.com/apps")
        default["aws_app_id"] = input("Onelogin App ID for AWS: ")
        print("\nOnelogin subdomain is 'company' for login domain of "
              "'comany.onelogin.com'")
        default["subdomain"] = input("Onelogin subdomain: ")

        print("\nAWS Role ARN is the ARN of the role you are logging into."
              "\nhttps://console.aws.amazon.com/iam/home?#/roles")
        default["aws_role_arn"] = input("AWS Role ARN: ")
        print("\nAWS Principal ARN is the ARN of the SAML provider."
              "\nhttps://console.aws.amazon.com/iam/home?#/providers")
        default["aws_principal_arn"] = input("AWS Principal ARN: ")

        config_fn = os.path.expanduser("~/{}".format(CONFIG_FILENAME))
        with open(config_fn, "w") as config_file:
            config.write(config_file)

        print("Configuration written to '{}'".format(config_fn))

    @staticmethod
    def load_config():
        config_fn = os.path.expanduser("~/{}".format(CONFIG_FILENAME))
        config = configparser.ConfigParser()
        config.read_file(open(config_fn))
        return config
