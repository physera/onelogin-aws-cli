import contextlib
from unittest import TestCase
from unittest.mock import patch

from io import StringIO

from onelogin_aws_cli.userquery import user_choice


class TestUser_choice(TestCase):

    def test_user_choice(self):
        mock_stdout = StringIO()

        with patch('builtins.input', side_effect=['2']):
            with contextlib.redirect_stdout(mock_stdout):
                result = user_choice('one', ['hallo', 'world', 'foobar'])

        output = mock_stdout.getvalue()
        assert result == "world"
        assert "Invalid option" not in output

    def test_user_choice_bad(self):
        mock_stdout = StringIO()

        with patch('builtins.input', side_effect=['bar', '2']):
            with contextlib.redirect_stdout(mock_stdout):
                result = user_choice('one', ['hallo', 'world', 'foo'])

        output = mock_stdout.getvalue()
        assert result == "world"
        assert "Invalid option" in output
