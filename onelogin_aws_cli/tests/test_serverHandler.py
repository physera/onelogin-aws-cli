import contextlib
from unittest import TestCase
from unittest.mock import MagicMock

from io import StringIO

from onelogin_aws_cli.daemon.server import ServerHandler


class TestServerHandler(TestCase):

    def test_handle(self):
        mock_config = {
            'recv.return_value': 'mock_input',
            'sendall.return_value': None
        }
        request_mock = MagicMock()
        request_mock.configure_mock(**mock_config)

        mock_stdout = StringIO()
        with contextlib.redirect_stdout(mock_stdout):
            ServerHandler(
                request=request_mock,
                client_address=('127.0.0.1', 90),
                server=None
            )

        request_mock.sendall.assert_called_once_with('MOCK_INPUT')
        request_mock.recv.assert_called_once_with(1024)

        self.assertEqual("""127.0.0.1 wrote:
mock_input
""", mock_stdout.getvalue())
