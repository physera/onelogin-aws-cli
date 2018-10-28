from argparse import Namespace
from unittest import TestCase, mock
from unittest.mock import MagicMock, patch

from onelogin_aws_cli import OneloginAWS


class _MockSection(Namespace):
    """
    Used to mock `onelogin_aws_cli.configuration.Section` objects
    """

    def __getitem__(self, item):
        return self.__getattribute__(item)

    def get(self, item):
        if hasattr(self, item):
            return self[item]
        return None


class TestOneloginSAML(TestCase):
    def setUp(self):
        """
        Set up mock SAML and base OneLoginAWS object
        """
        self.ol = OneloginAWS(
            _MockSection(
                base_uri="https://api.us.onelogin.com/",
                client_id='mock-id',
                client_secret='mock-secret',
                aws_app_id='mock-app-id',
                subdomain='example',
                can_save_password=False,
                username='mock-username',
                duration_seconds=2600,
                auto_determine_ip_address=False,
            ),
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
            get_saml_assertion_verifying=(
                self.get_saml_assertion_verifying_mock
            ),
            error=None,
        )

    @mock.patch('getpass.getpass')
    def test_get_saml_assertion_single(self, getpw):
        getpw.return_value = 'mock-password'
        with patch('builtins.input', side_effect=['123456']):
            self.ol.get_saml_assertion()

        self.assertEqual(self.ol.saml, 'mock-saml-response')

        self.get_saml_assertion_mock.assert_called_with(
            username_or_email='mock-username',
            password='mock-password',
            app_id='mock-app-id',
            subdomain='example',
            ip_address=None,
        )

        self.get_saml_assertion_verifying_mock.assert_called_with(
            'mock-app-id', 'mock-id-1',
            'mock-token', '123456'
        )

    @mock.patch('getpass.getpass')
    def test_get_saml_assertion_multiple(self, getpw):
        getpw.return_value = 'mock-password'
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
            username_or_email='mock-username',
            password='mock-password',
            app_id='mock-app-id',
            subdomain='example',
            ip_address=None,
        )

        self.get_saml_assertion_verifying_mock.assert_called_with(
            'mock-app-id', 'mock-id-2',
            'mock-token', '123456'
        )

    @patch('builtins.input', side_effect=['123456'])
    @mock.patch('getpass.getpass')
    def test_username_prompt(self, getpw, input):
        getpw.return_value = 'mock-password'
        self.ol.username = None
        self.ol.get_saml_assertion()

        self.assertEqual(self.ol.user_credentials.username, 'mock-username')
        self.assertEqual(self.ol.user_credentials.password, 'mock-password')

    def test_username_unspecified(self):
        ol = OneloginAWS(
            _MockSection(
                base_uri="https://api.us.onelogin.com/",
                client_id='mock-id',
                client_secret='mock-secret',
                aws_app_id='mock-app-id',
                subdomain='example',
                can_save_password=False,
                duration_seconds=2600,
                auto_determine_ip_address=False,
            ),
        )
        self.assertIsNone(ol.user_credentials.username)

    def tearDown(self):
        """
        Reset MagicMocks
        """
        self.get_saml_assertion_verifying_mock.reset_mock()
        self.get_saml_assertion_mock.reset_mock()
