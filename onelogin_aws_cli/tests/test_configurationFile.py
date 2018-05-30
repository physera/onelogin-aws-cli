from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from onelogin_aws_cli.configuration import ConfigurationFile
from onelogin_aws_cli.tests import helper


class TestConfigurationFile(TestCase):

    def test_can_save_password_username_true(self):
        cfg = helper.build_config("""[defaults]
save_password = true

[profile_test]
save_password = true""")
        self.assertTrue(cfg.section("profile_test").can_save_password)

    def test_can_save_password_username_false(self):
        cfg = helper.build_config("""[defaults]
save_password = false

[profile_test]
save_password = false""")
        self.assertFalse(cfg.section("profile_test").can_save_password)

    def test_can_save_password_username_xor_1(self):
        cfg = helper.build_config("""[defaults]
save_password = false

[profile_test]
save_password = true""")
        self.assertTrue(cfg.section("profile_test").can_save_password)

    def test_can_save_password_username_xor_2(self):
        cfg = helper.build_config("""[defaults]
save_password = true

[profile_test]
save_password = false""")
        self.assertFalse(cfg.section("profile_test").can_save_password)

    def test_can_save_password_username_inherit_true(self):
        cfg = helper.build_config("""[defaults]
save_password = false

[profile_test]""")
        self.assertFalse(cfg.section("profile_test").can_save_password)

    def test_can_save_password_username_inherit_false(self):
        cfg = helper.build_config("""[defaults]
save_password = true

[profile_test]""")
        self.assertTrue(cfg.section("profile_test").can_save_password)

    def test_can_save_password_username_defaults_false(self):
        cfg = helper.build_config("""[defaults]
save_password = false""")
        self.assertFalse(cfg.section("defaults").can_save_password)

    def test_can_save_password_username_defaults_true(self):
        cfg = helper.build_config("""[defaults]
save_password = true""")
        self.assertTrue(cfg.section("defaults").can_save_password)

    def test_initialise(self):
        str = StringIO()
        cfg = ConfigurationFile(str)
        with patch('builtins.input',
                   side_effect=['2', 'mock_client_id', 'mock_client_secret',
                                'mock_aws_app_id', 'mock_subdomain']):
            cfg.initialise()
        str.seek(0)

        self.assertEqual("""[defaults]
base_uri = https://api.eu.onelogin.com/
client_id = mock_client_id
client_secret = mock_client_secret
aws_app_id = mock_aws_app_id
subdomain = mock_subdomain

""", str.getvalue())

    def test_is_initialised(self):
        content = StringIO()
        cf = ConfigurationFile(content)
        self.assertFalse(cf.is_initialised)

        cf = helper.build_config("""[section]
first=foo""")
        self.assertTrue(cf.is_initialised)

        cf = helper.build_config("""[defaults]
first=foo""")
        self.assertTrue(cf.is_initialised)

    def test_section_get(self):
        cfg = helper.build_config("""[profile_test]
save_password = true""")
        self.assertTrue(cfg.section("profile_test").get("save_password"))

    def test_section_get_fallback(self):
        cfg = helper.build_config("""[profile_test]
""")
        self.assertFalse(cfg.section("profile_test").get("save_password"))

    def test_has_defaults(self):
        content = StringIO()
        cf = ConfigurationFile(content)
        self.assertFalse(cf.has_defaults)

        cf = helper.build_config("""[defaults]
first=foo""")
        self.assertTrue(cf.has_defaults)

    def test_supports_default(self):
        cf = helper.build_config("""[defaults]
first=foo""")
        self.assertEqual("defaults", cf.default_section)

        cf = helper.build_config("""[defaults]
first=foo

[default]
second=bar""")
        self.assertEqual("defaults", cf.default_section)
