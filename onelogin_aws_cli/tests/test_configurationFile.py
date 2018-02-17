from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from onelogin_aws_cli.configuration import ConfigurationFile


class TestConfigurationFile(TestCase):

    def test_can_save_password_username_true(self):
        str = StringIO()
        str.write("""[defaults]
save_password = false

[profile_test]
save_password = true""")
        str.seek(0)
        cfg = ConfigurationFile(str)
        self.assertTrue(cfg.section("profile_test").can_save_password)

    def test_can_save_password_username_false(self):
        str = StringIO()
        str.write("""[defaults]
save_password = false

[profile_test]
save_password = false""")
        str.seek(0)
        cfg = ConfigurationFile(str)
        self.assertFalse(cfg.section("profile_test").can_save_password)

    def test_can_save_password_username_xor_1(self):
        str = StringIO()
        str.write("""[defaults]
save_password = false

[profile_test]
save_password = true""")
        str.seek(0)
        cfg = ConfigurationFile(str)
        self.assertTrue(cfg.section("profile_test").can_save_password)

    def test_can_save_password_username_xor_2(self):
        str = StringIO()
        str.write("""[defaults]
save_password = false

[profile_test]
save_password = false""")
        str.seek(0)
        cfg = ConfigurationFile(str)
        self.assertFalse(cfg.section("profile_test").can_save_password)

    def test_can_save_password_username_xor_3(self):
        str = StringIO()
        str.write("""[defaults]
    save_password = false

[profile_test]""")
        str.seek(0)
        cfg = ConfigurationFile(str)
        self.assertFalse(cfg.section("profile_test").can_save_password)

    def test_initialise(self):
        str = StringIO()
        cfg = ConfigurationFile(str)
        with patch('builtins.input',
                   side_effect=['2', 'mock_client_id', 'mock_client_secret',
                                'mock_aws_app_id', 'mock_subdomain']):
            cfg.initialise()
        str.seek(0)

        self.assertEqual("""[default]
base_uri = https://api.eu.onelogin.com/
client_id = mock_client_id
client_secret = mock_client_secret
aws_app_id = mock_aws_app_id
subdomain = mock_subdomain

""", str.getvalue())
