from unittest import TestCase

from onelogin_aws_cli.argparse import OneLoginAWSArgumentParser


class TestOneLoginAWSArgumentParser(TestCase):
    def test_basic(self):
        parser = OneLoginAWSArgumentParser()
        args = parser.parse_args([
            '--version'
        ])

        self.assertEqual(args, [])

    def test_add_cli_options(self):
        self.fail()
