from unittest import TestCase

from onelogin_aws_cli.credsource import MissingCredentialException, \
    MissingMfaDeviceException, MissingMfaOtpException, \
    MissingPasswordException, MissingUsernameException


class TestMissingCredentialException(TestCase):
    def test_init(self):
        self.assertEqual(
            str(MissingCredentialException()),
            "ONELOGIN_error_MISSING"
        )

    def test_missing_username(self):
        self.assertEqual(
            str(MissingUsernameException()),
            "ONELOGIN_USERNAME_MISSING"
        )

    def test_missing_password(self):
        self.assertEqual(
            str(MissingPasswordException()),
            "ONELOGIN_PASSWORD_MISSING"
        )

    def test_missing_mfa_device(self):
        self.assertEqual(
            str(MissingMfaDeviceException()),
            "ONELOGIN_MFA_DEVICE_MISSING"
        )

    def test_missing_password_device(self):
        self.assertEqual(
            str(MissingMfaOtpException()),
            "ONELOGIN_MFA_OTP_MISSING"
        )
