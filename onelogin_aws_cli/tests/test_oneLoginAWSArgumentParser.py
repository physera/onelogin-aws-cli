import contextlib
from unittest import TestCase

import pkg_resources
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
            version + r'$'
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
            '-c'
        ])

        self.assertEqual(args.config_name, 'my_config')
        self.assertEqual(args.profile, 'my_profile')
        self.assertEqual(args.username, 'my_username')
        self.assertTrue(args.configure)
