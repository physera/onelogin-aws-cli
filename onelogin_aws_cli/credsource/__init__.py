"""
Handles multiple credentials sources
"""
from typing import List, Optional

from onelogin_aws_cli.model import CredentialType


class CredentialsSource(object):
    """
    Base class for objects which are used as sources for credentials
    """

    def __init__(self, provided_cred_types: List[CredentialType] = tuple(),
                 dependent_cred_types: List[CredentialType] = tuple()):
        self._cred_types = provided_cred_types
        self._dependent_cred_types = dependent_cred_types

    def can_handle(self, cred_type: CredentialType) -> bool:
        """
        True if this credentials source can handle that type of credential
        :param cred_type:
        :return:
        """

        return cred_type in self._cred_types

    def depends_on(self, cred_type: CredentialType) -> bool:
        """
        True if the credential source must be provided with credential supplied
        above.

        :param cred_type:
        :return:
        """
        return cred_type in self._dependent_cred_types

    def username(self, new_password=None) -> Optional[str]:
        """
        Should be overriden. Retrieves a OneLogin username
        """
        raise MissingUsernameException()

    def password(self, new_password=None) -> Optional[str]:
        """
        Should be overriden. Retrieves a OneLogin Password
        :return:
        """

        raise MissingPasswordException()

    def mfa_device(self, new_mfa_device=None) -> Optional[str]:
        """
        Should be overriden. Retrieves a OneLogin MFA Device
        :return:
        """

        raise MissingMfaDeviceException()

    def mfa_otp(self) -> str:
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


class ReadOnlyCredentialTypeException(Exception):
    """
    Called when a write operation is performed on a credential source.
    """

    def __init__(self, source: type, cred_type: CredentialType):
        super().__init__(
            "'{source}' is not able to write to '{cred_type}'".format(
                source=source.__name__,
                cred_type=cred_type.value
            )
        )
