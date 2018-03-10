import signal
from unittest import TestCase

from onelogin_aws_cli.model import SignalRepr


class TestSignalRepr(TestCase):
    def test_string_rep(self):
        for key, sig, enum in [
            ["SIGTERM", signal.SIGTERM, SignalRepr.SIGTERM],
            ["SIGINT", signal.SIGINT, SignalRepr.SIGINT]
        ]:
            self.assertEqual(int(sig), int(SignalRepr[key].value))
            self.assertEqual(enum, SignalRepr[key])
            self.assertEqual(str(enum), key)
