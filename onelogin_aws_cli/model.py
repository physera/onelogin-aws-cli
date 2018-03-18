"""
Describes data structures within the project
"""
import signal

from enum import Enum, auto


class SignalRepr(Enum):
    """
    Represent the signal types
    """

    SIGTERM = signal.SIGTERM
    SIGINT = signal.SIGINT

    def __str__(self):
        return str(self._name_)


class CredentialType(Enum):
    """
    Represent the types of Credentials
    """
    # Username
    USERNAME_R = auto()
    USERNAME_W = auto()
    USERNAME = USERNAME_R | USERNAME_W

    # Password
    PASSWORD_R = auto()
    PASSWORD_W = auto()
    PASSWORD = PASSWORD_R | PASSWORD_W

    MFA_DEVICE = auto()
    MFA_OTP = auto()


class CredentialSourceRequirement(Enum):
    """
    Defines whether or not a credential source is dependent on having another
    value set.
    """

    USERNAME = auto()
