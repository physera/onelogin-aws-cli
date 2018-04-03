import contextlib
from os import environ
from unittest import TestCase

import pkg_resources
import re
from io import StringIO

from onelogin_aws_cli.argparse import OneLoginAWSArgumentParser


class TestOneLoginAWSArgumentParser(TestCase):

    def test_basic(self):
        parser = OneLoginAWSArgumentParser()
        args = parser.parse_args([
            '-C', 'my_config',
            '--profile', 'my_profile',
            '-u', 'my_username'
        ])

        self.assertEqual(args.config_name, 'my_config')
        self.assertEqual(args.profile, 'my_profile')
        self.assertEqual(args.username, 'my_username')

    def test_version(self):
        parser = OneLoginAWSArgumentParser()
        parser.add_cli_options()
        mock_stdout = StringIO()

        with self.assertRaises(SystemExit) as cm:
            with contextlib.redirect_stdout(mock_stdout):
                parser.parse_args([
                    '--version'
                ])

        # This spits out the nosetest prog name.
        # I'm ok with that, as what is important is that the version is
        # correct
        version = pkg_resources.get_distribution('onelogin_aws_cli').version
        self.assertRegex(
            mock_stdout.getvalue(),
            re.escape(version) + r'$'
        )

        self.assertEqual(cm.exception.code, 0)

    def test_add_cli_options(self):
        parser = OneLoginAWSArgumentParser()
        parser.add_cli_options()
        args = parser.parse_args([
            '-C', 'my_config',
            '--profile', 'my_profile',
            '-u', 'my_username',
            '--renew-seconds', '30',
            '-c',
            '-d', '43200',
        ])

        self.assertEqual(args.config_name, 'my_config')
        self.assertEqual(args.profile, 'my_profile')
        self.assertEqual(args.username, 'my_username')
        self.assertEqual(args.renew_seconds, 30)
        self.assertTrue(args.configure)
        self.assertEqual(args.duration_seconds, 43200)

    def test_legacy_renew_seconds(self):
        parser = OneLoginAWSArgumentParser()
        parser.add_cli_options()
        args = parser.parse_args([
            '--renewSeconds', '30'
        ])

        self.assertEqual(args.renew_seconds_legacy, 30)

        with self.assertRaises(SystemExit) as cm:
            parser.parse_args([
                '--renewSeconds', '30',
                '--renew-seconds', '30',
            ])

        self.assertEqual(cm.exception.code, 2)

    def test_environment_variable(self):
        environ['ONELOGIN_AWS_CLI_CONFIG_NAME'] = 'mock-config'
        environ['ONELOGIN_AWS_CLI_PROFILE'] = 'mock-profile'
        environ['ONELOGIN_AWS_CLI_USERNAME'] = 'mock-username'
        environ['ONELOGIN_AWS_CLI_DURATION_SECONDS'] = '10'
        environ['ONELOGIN_AWS_CLI_RENEW_SECONDS'] = '10'

        parser = OneLoginAWSArgumentParser()

        args = parser.parse_args([])

        self.assertEqual('mock-config', args.config_name)
        self.assertEqual('mock-profile', args.profile)
        self.assertEqual('mock-username', args.username)
        self.assertEqual(10, args.renew_seconds)
        self.assertEqual(10, args.duration_seconds)

        del environ['ONELOGIN_AWS_CLI_CONFIG_NAME']
        del environ['ONELOGIN_AWS_CLI_PROFILE']
        del environ['ONELOGIN_AWS_CLI_USERNAME']
        del environ['ONELOGIN_AWS_CLI_DURATION_SECONDS']
        del environ['ONELOGIN_AWS_CLI_RENEW_SECONDS']
