import contextlib
import signal
from argparse import Namespace
from io import StringIO
from unittest import TestCase
from unittest.mock import MagicMock

from onelogin_aws_cli.cli import _set_interrupt_handler


class TestCli(TestCase):

    def test__get_interrupt_handler(self):
        method = MagicMock()
        handler = _set_interrupt_handler(
            interrupted=Namespace(set=method),
            process_type="mock"
        )

        mock_stdout = StringIO()

        with contextlib.redirect_stdout(mock_stdout):
            handler(signal.SIGTERM)

        method.assert_called_once_with()
        method.assert_called_with()

        self.assertEqual("""Received SIGTERM.
Shutting down mock process...
""", mock_stdout.getvalue())
