"""
Describes data structures within the project
"""
import signal

from enum import Enum, unique


class SignalRepr(Enum):
    """
    Represent the signal types
    """

    SIGTERM = signal.SIGTERM
    SIGINT = signal.SIGINT

    def __str__(self):
        return str(self._name_)


@unique
class CredentialType(Enum):
    """
    Represent the types of Credentials
    """
    USERNAME = 0b0001
    PASSWORD = 0b0010
    MFA_DEVICE = 0b0100
    MFA_OTP = 0b1000
