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
    USERNAME = auto()
    PASSWORD = auto()
    MFA_DEVICE = auto()
    MFA_OTP = auto()
