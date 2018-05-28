from unittest import TestCase
from unittest.mock import MagicMock

from onelogin_aws_cli.credentials import UserCredentials
from onelogin_aws_cli.tests import helper


class TestUserCredentials(TestCase):

    def test_load_password_promptuser(self):
        cfg = helper.build_config("""[test-section]
username = mock_user
""")
        sec = cfg.section("test-section")

        creds = UserCredentials(sec)
        creds._load_password_from_keychain = MagicMock()
        creds._prompt_user_password = MagicMock()
        creds._save_password_to_keychain = MagicMock()

        creds.load_password()

        creds._load_password_from_keychain.assert_not_called()
        creds._save_password_to_keychain.assert_not_called()

        creds._prompt_user_password.assert_called_once_with()

    def test_load_password_can_save_fail(self):
        cfg = helper.build_config("""[test-section]
username = mock_user
save_password = true
""")
        sec = cfg.section("test-section")

        creds = UserCredentials(sec)
        creds._load_password_from_keychain = MagicMock()
        creds._prompt_user_password = MagicMock()
        creds._save_password_to_keychain = MagicMock()

        with self.assertRaises(RuntimeError):
            creds.load_password()

        creds._load_password_from_keychain.assert_called_once_with()
        creds._prompt_user_password.assert_called_once_with()

        creds._save_password_to_keychain.assert_not_called()

    def test_save_password_success(self):
        cfg = helper.build_config("""[test-section]
username = mock_user
save_password = true
""")
        sec = cfg.section("test-section")

        creds = UserCredentials(sec)

        def create_password():
            creds.password = "mock"

        creds._load_password_from_keychain = MagicMock()
        creds._prompt_user_password = MagicMock(side_effect=create_password)
        creds._save_password_to_keychain = MagicMock()

        creds.load_password()

        creds._load_password_from_keychain.assert_called_once_with()
        creds._prompt_user_password.assert_called_once_with()
        creds._save_password_to_keychain.assert_called_once_with()
