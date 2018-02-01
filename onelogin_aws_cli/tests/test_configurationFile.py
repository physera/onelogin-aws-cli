from io import StringIO
from unittest import TestCase

from onelogin_aws_cli import ConfigurationFile


class TestConfigurationFile(TestCase):

    def test_can_save_password_username_true(self):
        str = StringIO()
        str.write("""[config onelogin-aws-login]
save_username = true
save_password = true""")
        str.seek(0)
        cfg = ConfigurationFile(str)
        self.assertTrue(cfg.can_save_username)
        self.assertTrue(cfg.can_save_password)

    def test_can_save_password_username_false(self):
        str = StringIO()
        str.write("""[config onelogin-aws-login]
save_username = true
save_password = true""")
        str.seek(0)
        cfg = ConfigurationFile(str)
        self.assertFalse(cfg.can_save_username)
        self.assertFalse(cfg.can_save_password)

    def test_can_save_password_username_xor_1(self):
        str = StringIO()
        str.write("""[config onelogin-aws-login]
save_username = false
save_password = true""")
        str.seek(0)
        cfg = ConfigurationFile(str)
        self.assertFalse(cfg.can_save_username)
        self.assertTrue(cfg.can_save_password)

    def test_can_save_password_username_xor_2(self):
        str = StringIO()
        str.write("""[config onelogin-aws-login]
save_username = true
save_password = false""")
        str.seek(0)
        cfg = ConfigurationFile(str)
        self.assertTrue(cfg.can_save_username)
        self.assertFalse(cfg.can_save_password)
