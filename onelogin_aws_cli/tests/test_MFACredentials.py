import contextlib
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from onelogin.api.models.device import Device

from onelogin_aws_cli import MFACredentials


class TestMFACredentials(TestCase):

    def setUp(self):
        self.mfa = MFACredentials()

    def test_has_device(self):
        self.assertFalse(self.mfa.has_device)

        self.mfa._device_index = 1
        self.assertFalse(self.mfa.has_device)

        self.mfa._device_index = None
        self.mfa._devices = [Device(dict())]
        self.assertFalse(self.mfa.has_device)

        self.mfa._device_index = 0
        self.assertTrue(self.mfa.has_device)

    def test_has_otp(self):
        self.assertFalse(self.mfa.has_otp)

        self.mfa._otp = 23487
        self.assertTrue(self.mfa.has_otp)

    def test_device(self):
        with self.assertRaises(TypeError):
            self.mfa.device

        self.mfa._devices = [Device(dict(
            device_id='mock_device_id'
        ))]
        self.mfa._device_index = 0

        device = self.mfa.device

        self.assertEqual(device.id, 'mock_device_id')

    def test_otp(self):
        self.assertIsNone(self.mfa.otp)

        self.mfa._otp = 23487
        self.assertEqual(self.mfa.otp, 23487)

    def test_ready(self):
        self.assertFalse(self.mfa.ready())

        self.mfa._device_index = 0
        self.mfa._devices = [Device(dict(
            device_id='mock_device_id'
        ))]
        self.mfa._otp = 23487

        self.assertTrue(self.mfa.ready())

    def test_reset(self):
        self.mfa._device_index = 0
        self.mfa._devices = [Device(dict(
            device_id='mock_device_id'
        ))]
        self.mfa._otp = 23487

        self.assertEqual(self.mfa._device_index, 0)
        self.assertEqual(self.mfa._devices[0].id, 'mock_device_id')
        self.assertEqual(self.mfa.otp, 23487)

        self.mfa.reset()

        self.assertIsNone(self.mfa._device_index)
        self.assertListEqual(self.mfa._devices, [])
        self.assertIsNone(self.mfa.otp)

    def test_select_device(self):
        self.mfa.select_device([
            Device(dict(device_id='1'))
        ])
        self.assertEqual(self.mfa._device_index, 0)
        self.assertEqual(self.mfa.device.id, '1')

        with patch('builtins.input', side_effect=['3']):
            self.mfa.select_device([
                Device(dict(device_id='1')),
                Device(dict(device_id='2')),
                Device(dict(device_id='3'))
            ])

        self.assertEqual(self.mfa.device.id, '3')

    def test_prompt_token(self):
        self.mfa.select_device([
            Device(dict(device_id='1', device_type='mock_device'))
        ])
        with patch('builtins.input', side_effect=['123456']):
            self.mfa.prompt_token()

        self.assertEqual(self.mfa.otp, '123456')

    def test_prompt_text(self):
        self.mfa.select_device([
            Device(dict(device_id='1', device_type='mock_device'))
        ])

        mock_stdout = StringIO()

        with patch('builtins.input', side_effect=['1'])as prompt:
            with contextlib.redirect_stdout(mock_stdout):
                self.mfa.prompt_token()

        prompt.assert_called_with('mock_device Token: ')
