import base64
import os
from argparse import Namespace
from unittest import TestCase
from unittest.mock import MagicMock, patch

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
        ), Namespace(
            username='mock-username',
            duration_seconds=2600
        ))

    def test_init(self):
        mock_config = dict(
            base_uri="https://api.us.onelogin.com/",
            client_id='mock-id',
            client_secret='mock-secret'
        )
        mock_args = Namespace(
            username='mock-username',
            duration_seconds=2600
        )
        ol = OneloginAWS(mock_config, mock_args)

        self.assertEqual(mock_config, ol.config)
        self.assertEqual(mock_args, ol.args)
        self.assertEqual('mock-username', ol.user_credentials.username)

    def test_get_arns(self):
        self.ol.saml = Namespace(saml_response=self.SAML_SINGLE_ROLE)
        self.ol.get_arns()

        self.assertEqual(
            [(self.ROLE_PREFIX, self.PRVD_PREFIX)],
            self.ol.all_roles
        )

    def test_get_arns_multi(self):
        self.ol.saml = Namespace(saml_response=self.SAML_MULTI_ROLE)
        self.ol.get_arns()

        self.assertEqual(
            (self.ROLE_PREFIX + '0', self.PRVD_PREFIX + '0'),
            self.ol.all_roles[0]
        )
        self.assertEqual(
            (self.ROLE_PREFIX + '1', self.PRVD_PREFIX + '1'),
            self.ol.all_roles[1]
        )
        self.assertEqual(
            (self.ROLE_PREFIX + '2', self.PRVD_PREFIX + '1'),
            self.ol.all_roles[2]
        )

    def test_get_role(self):
        self.ol.saml = Namespace(saml_response=self.SAML_SINGLE_ROLE)
        self.ol.get_role()

        self.assertEqual(self.ROLE_PREFIX, self.ol.role_arn)
        self.assertEqual(self.PRVD_PREFIX, self.ol.principal_arn)

    def test_get_role_multi(self):
        self.ol.saml = Namespace(saml_response=self.SAML_MULTI_ROLE)
        with patch('builtins.input', side_effect=['2']):
            self.ol.get_role()

        self.assertEqual(self.ROLE_PREFIX + "2", self.ol.role_arn)
        self.assertEqual(self.PRVD_PREFIX + "1", self.ol.principal_arn)

    def test_get_role_fail(self):
        self.ol.all_roles = []
        self.ol.get_arns = MagicMock()
        with self.assertRaisesRegex(Exception, r'^No roles found$'):
            self.ol.get_role()
