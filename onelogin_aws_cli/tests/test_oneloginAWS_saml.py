from argparse import Namespace
from unittest import TestCase
from unittest.mock import MagicMock, patch

from onelogin_aws_cli import OneloginAWS


class TestOneloginSAML(TestCase):
    def setUp(self):
        """
        Set up mock SAML and base OneLoginAWS object
        """
        self.ol = OneloginAWS(dict(
            base_uri="https://api.us.onelogin.com/",
            client_id='mock-id',
            client_secret='mock-secret',
            aws_app_id='mock-app-id',
            subdomain='example'
        ), Namespace(
            username='mock-username'
        ))
        self.ol.password = "mock-password"

    def test_get_saml_assertion_single(self):
        get_saml_assertion_mock = MagicMock(return_value=Namespace(
            mfa=Namespace(
                devices=[
                    Namespace(
                        type='mock',
                        id='mock-id'
                    )
                ],
                state_token='mock-token'
            ),
        ))
        get_saml_assertion_verifying_mock = MagicMock(
            return_value='mock-saml-response'
        )
        self.ol.ol_client = Namespace(
            get_saml_assertion=get_saml_assertion_mock,
            get_saml_assertion_verifying=get_saml_assertion_verifying_mock
        )
        with patch('builtins.input', side_effect=['123456']):
            self.ol.get_saml_assertion()

        self.assertEqual(self.ol.saml, 'mock-saml-response')
