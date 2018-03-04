from argparse import Namespace
from unittest import TestCase
from unittest.mock import MagicMock, patch

from onelogin_aws_cli import OneloginAWS


class TestOneloginSAML(TestCase):
    def setUp(self):
        """
        Set up mock SAML and base OneLoginAWS object
        """
        self.ol = OneloginAWS(
            dict(
                base_uri="https://api.us.onelogin.com/",
                client_id='mock-id',
                client_secret='mock-secret',
                aws_app_id='mock-app-id',
                subdomain='example'
            ),
            Namespace(username='mock-username')
        )

        self.ol.password = "mock-password"

        self.get_saml_assertion_mock = MagicMock(return_value=Namespace(
            mfa=Namespace(
                devices=[Namespace(type='mock1', id='mock-id-1'), ],
                state_token='mock-token'
            ),
        ))
        self.get_saml_assertion_verifying_mock = MagicMock(
            return_value='mock-saml-response'
        )
        self.ol.ol_client = Namespace(
            get_saml_assertion=self.get_saml_assertion_mock,
            get_saml_assertion_verifying=self.get_saml_assertion_verifying_mock
        )

    def test_get_saml_assertion_single(self):
        with patch('builtins.input', side_effect=['123456']):
            self.ol.get_saml_assertion()

        self.assertEqual(self.ol.saml, 'mock-saml-response')

        self.get_saml_assertion_mock.assert_called_with(
            'mock-username', 'mock-password',
            'mock-app-id', 'example'
        )

        self.get_saml_assertion_verifying_mock.assert_called_with(
            'mock-app-id', 'mock-id-1',
            'mock-token', '123456'
        )

    def test_get_saml_assertion_multiple(self):
        self.get_saml_assertion_mock = MagicMock(return_value=Namespace(
            mfa=Namespace(
                devices=[
                    Namespace(type='mock1', id='mock-id-1'),
                    Namespace(type='mock2', id='mock-id-2'),
                    Namespace(type='mock3', id='mock-id-3')
                ],
                state_token='mock-token'
            ),
        ))

        self.ol.ol_client.get_saml_assertion = self.get_saml_assertion_mock

        with patch('builtins.input', side_effect=['2', '123456']):
            self.ol.get_saml_assertion()

        self.assertEqual(self.ol.saml, 'mock-saml-response')

        self.get_saml_assertion_mock.assert_called_with(
            'mock-username', 'mock-password',
            'mock-app-id', 'example'
        )

        self.get_saml_assertion_verifying_mock.assert_called_with(
            'mock-app-id', 'mock-id-2',
            'mock-token', '123456'
        )

    def test_username_prompt(self):
        with patch('builtins.input',
                   side_effect=['mock-password', '2', '123456']):
            self.ol.username = None
            self.ol.get_saml_assertion()

        self.assertEqual(self.ol.username, 'mock-password')

    def tearDown(self):
        """
        Reset MagicMocks
        """
        self.get_saml_assertion_verifying_mock.reset_mock()
        self.get_saml_assertion_mock.reset_mock()
