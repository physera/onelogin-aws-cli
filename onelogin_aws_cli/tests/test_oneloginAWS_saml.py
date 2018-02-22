from argparse import Namespace
from unittest.mock import MagicMock

from onelogin_aws_cli import OneloginAWS
from onelogin_aws_cli.tests.test_oneloginAWS import TestOneloginAWS


class TestOneloginSAML(TestOneloginAWS):
    def setUp(self):
        """
        Set up mock SAML and base OneLoginAWS object
        """
        self.ol = OneloginAWS(dict(
            base_uri="https://api.us.onelogin.com/",
            client_id='mock-id',
            client_secret='mock-secret'
        ), Namespace(username='mock-username'))
        self.ol

    def test_get_saml_assertion(self):
        get_saml_assertion_verifying_mock = MagicMock(return_value=Namespace())
        self.ol.ol_client = Namespace(
            get_saml_assertion_verifying=get_saml_assertion_verifying_mock
        )
