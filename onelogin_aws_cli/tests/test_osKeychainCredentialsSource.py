from unittest import TestCase, mock

from onelogin_aws_cli.credsource.oskeychain import OsKeychainCredentialsSource
from onelogin_aws_cli.model import CredentialType


class TestOsKeychainCredentialsSource(TestCase):
    def test_init(self):
        src = OsKeychainCredentialsSource()

        self.assertTrue(src.can_handle(CredentialType.PASSWORD))
        self.assertFalse(src.can_handle(CredentialType.USERNAME))
        self.assertFalse(src.can_handle(CredentialType.MFA_DEVICE))
        self.assertFalse(src.can_handle(CredentialType.MFA_OTP))

        self.assertFalse(src.depends_on(CredentialType.PASSWORD))
        self.assertTrue(src.depends_on(CredentialType.USERNAME))
        self.assertFalse(src.depends_on(CredentialType.MFA_DEVICE))
        self.assertFalse(src.depends_on(CredentialType.MFA_OTP))

    @mock.patch('keyring.set_password')
    def test_password_write(self, mock_gp_w):
        src = OsKeychainCredentialsSource()
        src.username("mock_username")
        src.password("mock_password")

        mock_gp_w.assert_called_with("onelogin-aws-cli", "mock_username",
                                     "mock_password")

    @mock.patch('keyring.get_password')
    def test_password_read(self, mock_gp_r):
        mock_gp_r.return_value = 'mock_password'
        src = OsKeychainCredentialsSource()
        src.username("mock_username")
        password = src.password()

        self.assertEqual(password, 'mock_password')

        mock_gp_r.assert_called_with('onelogin-aws-cli', 'mock_username')

    def test_username(self):
        src = OsKeychainCredentialsSource()
        src.username("mock_username")

        self.assertEqual(src.username(), "mock_username")
