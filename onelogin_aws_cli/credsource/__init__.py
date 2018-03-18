"""
Handles multiple credentials sources
"""
from typing import List

from onelogin_aws_cli.model import CredentialType


class CredentialsSource(object):
    """
    Base class for objects which are used as sources for credentials
    """

    def __init__(self, supported_cred_types: List[CredentialType] = tuple()):
        self._cred_types = supported_cred_types

    def can_handle(self, cred_type: CredentialType) -> bool:
        """
        True if this credentials source can handle that type of credential
        :param cred_type:
        :return:
        """

        return cred_type in self._cred_types

    def __call__(self, *args, **kwargs):
        pass
