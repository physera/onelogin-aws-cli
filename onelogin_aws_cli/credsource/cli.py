"""
CLI credentials source. Will prompt the user.
"""

from onelogin_aws_cli.credsource import CredentialsSource
from onelogin_aws_cli.model import CredentialType


class CliCredentialsSource(CredentialsSource):
    """
    Prompts the user for credentials sources
    """

    def __init__(self):
        super().__init__(supported_cred_types=[
            CredentialType.USERNAME,
            CredentialType.PASSWORD,
            CredentialType.MFA_DEVICE,
            CredentialType.MFA_OTP
        ])
