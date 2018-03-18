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

    def username(self):
        """
        Should be overriden. Retrieves a OneLogin username
        """
        raise MissingUsernameException()

    def password(self):
        """
        Should be overriden. Retrieves a OneLogin Password
        :return:
        """

        raise MissingPasswordException()

    def mfa_device(self):
        """
        Should be overriden. Retrieves a OneLogin MFA Device
        :return:
        """

        raise MissingMfaDeviceException()

    def mfa_otp(self):
        """
        Should be overriden. Retrieves a OneLogin MFA OTP
        :return:
        """

        raise MissingMfaOtpException()


class MissingCredentialException(Exception):
    """
    Raised when a credential is missing.
    """
    TYPE = "error"

    def __init__(self):
        super().__init__("ONELOGIN_" + self.TYPE + "_MISSING")


class MissingPasswordException(MissingCredentialException):
    """
    Throw when a required password can not be found
    """
    TYPE = "PASSWORD"


class MissingUsernameException(MissingCredentialException):
    """
    Throw when a required password can not be found
    """
    TYPE = "USERNAME"


class MissingMfaDeviceException(MissingCredentialException):
    """
    Throw when a required password can not be found
    """
    TYPE = "MFA_DEVICE"


class MissingMfaOtpException(MissingCredentialException):
    """
    Throw when a required password can not be found
    """
    TYPE = "MFA_OTP"
