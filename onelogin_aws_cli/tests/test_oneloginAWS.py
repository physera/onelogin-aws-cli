import base64
from argparse import Namespace
from unittest import TestCase
from unittest.mock import patch

from onelogin_aws_cli import OneloginAWS


class TestOneloginAWS(TestCase):
    ROLE_PREFIX = "arn:aws:iam::012345678901:role/OneLogin-MyRole"
    PRVD_PREFIX = "arn:aws:iam::012345678901:saml-provider/OneLogin-MyProvider"

    def setUp(self):
        with open('fixtures/SAML_SINGLE_ROLE.xml', 'rb') as fp:
            self.SAML_SINGLE_ROLE = base64.b64encode(fp.read())
        with open('fixtures/SAML_MULTI_ROLE.xml', 'rb') as fp:
            self.SAML_MULTI_ROLE = base64.b64encode(fp.read())

    def test_init(self):
        mock_config = dict()
        mock_args = Namespace(username='mock-username')
        ol = OneloginAWS(mock_config, mock_args)

        assert mock_config == ol.config
        assert mock_args == ol.args
        assert 'mock-username' == ol.username

    def test_get_arns(self):
        ol = OneloginAWS(dict(), Namespace(username='mock-username'))
        ol.saml = self.SAML_SINGLE_ROLE
        ol.get_arns()

        assert [(self.ROLE_PREFIX, self.PRVD_PREFIX)] == ol.all_roles

    def test_get_arns_multi(self):
        ol = OneloginAWS(dict(), Namespace(username='mock-username'))
        ol.saml = self.SAML_MULTI_ROLE
        ol.get_arns()

        assert (self.ROLE_PREFIX + '0',
                self.PRVD_PREFIX + '0') == ol.all_roles[0]
        assert (self.ROLE_PREFIX + '1',
                self.PRVD_PREFIX + '1') == ol.all_roles[1]
        assert (self.ROLE_PREFIX + '2',
                self.PRVD_PREFIX + '1') == ol.all_roles[2]

    def test_get_role(self):
        ol = OneloginAWS(dict(), Namespace(username='mock-username'))
        ol.saml = self.SAML_SINGLE_ROLE
        ol.get_role()

        assert self.ROLE_PREFIX == ol.role_arn
        assert self.PRVD_PREFIX == ol.principal_arn

    def test_get_role_multi(self):
        ol = OneloginAWS(dict(), Namespace(username='mock-username'))
        ol.saml = self.SAML_MULTI_ROLE
        with patch('builtins.input', side_effect=['2']):
            ol.get_role()

        assert self.ROLE_PREFIX + "2" == ol.role_arn
        assert self.PRVD_PREFIX + "1" == ol.principal_arn
