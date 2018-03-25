from unittest import TestCase

from onelogin_aws_cli.credsource import CredentialsSource, \
    MissingMfaDeviceException, MissingMfaOtpException, \
    MissingPasswordException, MissingUsernameException


class TestCredentialsSource(TestCase):
    def test_can_handle_default(self):
        src = CredentialsSource()

        with self.assertRaises(MissingUsernameException):
            src.username()

        with self.assertRaises(MissingPasswordException):
            src.password()

        with self.assertRaises(MissingMfaDeviceException):
            src.mfa_device()

        with self.assertRaises(MissingMfaOtpException):
            src.mfa_otp()
