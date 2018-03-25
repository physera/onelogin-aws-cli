import contextlib
import signal
from argparse import Namespace
from io import StringIO
from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch

from onelogin_aws_cli.cli import _load_config, _set_interrupt_handler


class TestCli(TestCase):

    def test__get_interrupt_handler(self):
        method = MagicMock()
        handler = _set_interrupt_handler(
            event=Namespace(set=method),
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

    def test__load_config(self):
        args = Namespace(config_name='mock_config')
        parser_mock = MagicMock()
        parser_mock.configure_mock(**{
            'parse_args.return_value': args,
        })

        config_mock = MagicMock()
        config_mock.configure_mock(**{
            'section.return_value': 'mock_section',
            'load.return_value': None
        })

        open_name = 'onelogin_aws_cli.cli.open'
        with patch(open_name, mock_open(read_data='foobar')):
            config_section, cli_args = _load_config(
                parser=parser_mock,
                config_file=config_mock,
                interactive=False
            )
        self.assertEqual(args, cli_args)
        self.assertEqual("mock_section", config_section)

        config_mock.load.called_once_with("")
