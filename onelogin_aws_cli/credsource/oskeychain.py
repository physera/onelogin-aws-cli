"""
CLI credentials source. Will prompt the user.
"""
from typing import Optional

import keyring

from onelogin_aws_cli.credsource import CredentialsSource
from onelogin_aws_cli.model import CredentialType


class OsKeychainCredentialsSource(CredentialsSource):
    """
    Prompts the user for credentials sources
    """
    SERVICE_NAME = "onelogin-aws-cli"

    def __init__(self):
        super().__init__(
            provided_cred_types=[
                CredentialType.PASSWORD,
            ],
            dependent_cred_types=[
                CredentialType.USERNAME
            ]
        )

        # Used for dependency only
        self._username = None

    def password(self, new_password=None) -> Optional[str]:
        """
        Read and write the password to and from the credential source
        """
        if new_password is None:
            return keyring.get_password(self.SERVICE_NAME, self._username)
        else:
            # No need to cache in memory.
            # This should always be available.
            keyring.set_password(self.SERVICE_NAME, self._username,
                                 new_password)

    def username(self, new_username=None):
        """
        Used only as a way to get the password in
        :param new_username:
        """
        if new_username is not None:
            self._username = new_username
        else:
            return self._username
