"""
CLI credentials source. Will prompt the user.
"""

from onelogin_aws_cli.credsource import CredentialsSource
from onelogin_aws_cli.model import CredentialType


class OsKeychainCredentialsSource(CredentialsSource):
    """
    Prompts the user for credentials sources
    """
    SERVICE_NAME = "onelogin-aws-cli"

    def __init__(self):
        super().__init__(supported_cred_types=[
            CredentialType.PASSWORD,
        ])
