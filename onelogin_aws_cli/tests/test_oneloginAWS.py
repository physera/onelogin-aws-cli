import base64
from argparse import Namespace
from unittest import TestCase
from unittest.mock import patch

from onelogin_aws_cli import OneloginAWS


class TestOneloginAWS(TestCase):
    MOCK_SAML_ASSERTION_SINGLE_ROLE = base64.b64encode("""<?xml version="1.0"?>
<samlp:Response xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion" xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">
    <saml:Assertion>
        <saml:AttributeStatement>
            <saml:Attribute Name="https://aws.amazon.com/SAML/Attributes/Role" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic">
                <saml:AttributeValue xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">arn:aws:iam::012345678901:role/OneLogin-MyRole,arn:aws:iam::012345678901:saml-provider/OneLogin-MyProvider</saml:AttributeValue>
            </saml:Attribute>
        </saml:AttributeStatement>
    </saml:Assertion>
</samlp:Response>
""".encode())

    MOCK_SAML_ASSERTION_MULTI_ROLE = base64.b64encode("""<?xml version="1.0"?>
    <samlp:Response xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion" xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">
        <saml:Assertion>
            <saml:AttributeStatement>
                <saml:Attribute Name="https://aws.amazon.com/SAML/Attributes/Role" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic">
                    <saml:AttributeValue xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">arn:aws:iam::012345678901:role/OneLogin-MyRole0,arn:aws:iam::012345678901:saml-provider/OneLogin-MyProvider0</saml:AttributeValue>
                    <saml:AttributeValue xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">arn:aws:iam::012345678901:role/OneLogin-MyRole1,arn:aws:iam::012345678901:saml-provider/OneLogin-MyProvider1</saml:AttributeValue>
                    <saml:AttributeValue xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">arn:aws:iam::012345678901:role/OneLogin-MyRole2,arn:aws:iam::012345678901:saml-provider/OneLogin-MyProvider1</saml:AttributeValue>
                </saml:Attribute>
            </saml:AttributeStatement>
        </saml:Assertion>
    </samlp:Response>
    """.encode())

    def test_init(self):
        mock_config = dict()
        mock_args = Namespace(username='mock-username')
        ol = OneloginAWS(mock_config, mock_args)

        assert mock_config == ol.config
        assert mock_args == ol.args
        assert 'mock-username' == ol.username
        assert 'STS' == type(ol.sts_client).__name__

    def test_get_arns(self):
        ol = OneloginAWS(dict(), Namespace(username='mock-username'))
        ol.saml = self.MOCK_SAML_ASSERTION_SINGLE_ROLE
        ol.get_arns()

        assert [('arn:aws:iam::012345678901:role/OneLogin-MyRole',
                 'arn:aws:iam::012345678901:saml-provider/OneLogin-MyProvider')] == ol.all_roles

    def test_get_arns_multi(self):
        ol = OneloginAWS(dict(), Namespace(username='mock-username'))
        ol.saml = self.MOCK_SAML_ASSERTION_MULTI_ROLE
        ol.get_arns()

        assert ('arn:aws:iam::012345678901:role/OneLogin-MyRole0',
                'arn:aws:iam::012345678901:saml-provider/OneLogin-MyProvider0') == ol.all_roles[0]
        assert ('arn:aws:iam::012345678901:role/OneLogin-MyRole1',
                'arn:aws:iam::012345678901:saml-provider/OneLogin-MyProvider1') == ol.all_roles[1]
        assert ('arn:aws:iam::012345678901:role/OneLogin-MyRole2',
                'arn:aws:iam::012345678901:saml-provider/OneLogin-MyProvider1') == ol.all_roles[2]

    def test_get_role(self):
        ol = OneloginAWS(dict(), Namespace(username='mock-username'))
        ol.saml = self.MOCK_SAML_ASSERTION_SINGLE_ROLE
        ol.get_role()

        assert "arn:aws:iam::012345678901:role/OneLogin-MyRole" == ol.role_arn
        assert 'arn:aws:iam::012345678901:saml-provider/OneLogin-MyProvider' == ol.principal_arn

    def test_get_role_multi(self):
        ol = OneloginAWS(dict(), Namespace(username='mock-username'))
        ol.saml = self.MOCK_SAML_ASSERTION_MULTI_ROLE
        with patch('builtins.input', side_effect=['2']):
            ol.get_role()

        assert "arn:aws:iam::012345678901:role/OneLogin-MyRole2" == ol.role_arn
        assert "arn:aws:iam::012345678901:saml-provider/OneLogin-MyProvider1" == ol.principal_arn
