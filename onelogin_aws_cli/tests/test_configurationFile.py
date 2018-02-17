from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from onelogin_aws_cli.configuration import ConfigurationFile


class TestConfigurationFile(TestCase):

    def _helper_build_config(self, config_content: str):
        str = StringIO()
        str.write(config_content)
        str.seek(0)
        return ConfigurationFile(str)

    def test_can_save_password_username_true(self):
        cfg = self._helper_build_config("""[defaults]
save_password = false

[profile_test]
save_password = true""")
        self.assertTrue(cfg.section("profile_test").can_save_password)

    def test_can_save_password_username_false(self):
        cfg = self._helper_build_config("""[defaults]
save_password = false

[profile_test]
save_password = false""")
        self.assertFalse(cfg.section("profile_test").can_save_password)

    def test_can_save_password_username_xor_1(self):
        cfg = self._helper_build_config("""[defaults]
save_password = false

[profile_test]
save_password = true""")
        self.assertTrue(cfg.section("profile_test").can_save_password)

    def test_can_save_password_username_xor_2(self):
        cfg = self._helper_build_config("""[defaults]
save_password = true

[profile_test]
save_password = false""")
        self.assertFalse(cfg.section("profile_test").can_save_password)

    def test_can_save_password_username_inherit_true(self):
        cfg = self._helper_build_config("""[defaults]
save_password = false

[profile_test]""")
        self.assertFalse(cfg.section("profile_test").can_save_password)

    def test_can_save_password_username_inherit_false(self):
        cfg = self._helper_build_config("""[defaults]
save_password = true

[profile_test]""")
        self.assertTrue(cfg.section("profile_test").can_save_password)

    def test_initialise(self):
        str = StringIO()
        cfg = ConfigurationFile(str)
        with patch('builtins.input',
                   side_effect=['2', 'mock_client_id', 'mock_client_secret',
                                'mock_aws_app_id', 'mock_subdomain']):
            cfg.initialise()
        str.seek(0)

        self.assertEqual("""[defaults]
save_password = False

[default]
base_uri = https://api.eu.onelogin.com/
client_id = mock_client_id
client_secret = mock_client_secret
aws_app_id = mock_aws_app_id
subdomain = mock_subdomain

""", str.getvalue())
