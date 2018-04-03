import os
from unittest import TestCase

from onelogin_aws_cli.argparse import EnvDefault


class TestEnvDefault(TestCase):
    def test_suceeds(self):
        os.environ['testEnv'] = 'this_value'
        env_object = EnvDefault(
            'testEnv',
            option_strings='--test-env',
            dest='test_env'
        )

        self.assertEqual(env_object.default, os.environ['testEnv'])

    def test_suceeds_no_env(self):
        del os.environ['testEnv']
        env_object = EnvDefault(
            'testEnv',
            option_strings='--test-env',
            dest='test_env'
        )

        self.assertIsNone(env_object.default)
