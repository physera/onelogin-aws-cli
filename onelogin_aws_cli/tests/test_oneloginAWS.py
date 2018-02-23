from argparse import Namespace
from unittest import TestCase
from unittest.mock import patch, MagicMock

import base64
import os

from onelogin_aws_cli import OneloginAWS

TEST_ROOT = os.path.join(os.path.dirname(__file__), "fixtures")


class TestOneloginAWS(TestCase):
    ROLE_PREFIX = "arn:aws:iam::123456789012:role/OneLogin-MyRole"
    PRVD_PREFIX = "arn:aws:iam::123456789012:saml-provider/OneLogin-MyProvider"

    def setUp(self):
        """
        Set up mock SAML and base OnloginAWS object
        """
        with open(os.path.join(TEST_ROOT, 'saml_single_role.xml'), 'rb') as fp:
            self.SAML_SINGLE_ROLE = base64.b64encode(fp.read())
        with open(os.path.join(TEST_ROOT, 'saml_multi_role.xml'), 'rb') as fp:
            self.SAML_MULTI_ROLE = base64.b64encode(fp.read())

        self.ol = OneloginAWS(dict(
            base_uri="https://api.us.onelogin.com/",
            client_id='mock-id',
            client_secret='mock-secret'
        ), Namespace(username='mock-username'))

    def test_init(self):
        mock_config = dict(
            base_uri="https://api.us.onelogin.com/",
            client_id='mock-id',
            client_secret='mock-secret'
        )
        mock_args = Namespace(username='mock-username')
        ol = OneloginAWS(mock_config, mock_args)

        assert mock_config == ol.config
        assert mock_args == ol.args
        assert 'mock-username' == ol.username

    def test_get_arns(self):
        self.ol.saml = Namespace(saml_response=self.SAML_SINGLE_ROLE)
        self.ol.get_arns()

        assert [(self.ROLE_PREFIX, self.PRVD_PREFIX)] == self.ol.all_roles

    def test_get_arns_multi(self):
        self.ol.saml = Namespace(saml_response=self.SAML_MULTI_ROLE)
        self.ol.get_arns()

        assert (self.ROLE_PREFIX + '0',
                self.PRVD_PREFIX + '0') == self.ol.all_roles[0]
        assert (self.ROLE_PREFIX + '1',
                self.PRVD_PREFIX + '1') == self.ol.all_roles[1]
        assert (self.ROLE_PREFIX + '2',
                self.PRVD_PREFIX + '1') == self.ol.all_roles[2]

    def test_get_role(self):
        self.ol.saml = Namespace(saml_response=self.SAML_SINGLE_ROLE)
        self.ol.get_role()

        assert self.ROLE_PREFIX == self.ol.role_arn
        assert self.PRVD_PREFIX == self.ol.principal_arn

    def test_get_role_multi(self):
        self.ol.saml = Namespace(saml_response=self.SAML_MULTI_ROLE)
        with patch('builtins.input', side_effect=['2']):
            self.ol.get_role()

        assert self.ROLE_PREFIX + "2" == self.ol.role_arn
        assert self.PRVD_PREFIX + "1" == self.ol.principal_arn

    def test_get_role_fail(self):
        self.ol.all_roles = []
        self.ol.get_arns = MagicMock()
        with self.assertRaisesRegex(Exception, r'^No roles found$'):
            self.ol.get_role()
