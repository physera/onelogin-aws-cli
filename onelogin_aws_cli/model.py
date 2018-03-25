"""
Describes data structures within the project
"""
import signal

from enum import Enum


class SignalRepr(Enum):
    """Represent the signal types"""

    SIGTERM = signal.SIGTERM
    SIGINT = signal.SIGINT

    def __str__(self):
        return str(self._name_)
