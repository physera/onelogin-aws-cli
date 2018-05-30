"""
Argument Parser
"""

import argparse
import os

import pkg_resources


class OneLoginAWSArgumentParser(argparse.ArgumentParser):
    """Argument Parser separated into daemon and cli tool"""

    def __init__(self):
        super().__init__(description='Login to AWS with OneLogin')

        self.add_argument(
            '-C', '--config-name',
            action=EnvDefault, required=False,
            dest='config_name', default='defaults',
            help='Switch configuration name within config file'
        )

        self.add_argument(
            '--profile',
            action=EnvDefault, required=False,
            help='Specify profile name of credential',
        )

        self.add_argument(
            '-u', '--username',
            action=EnvDefault, required=False,
            help='Specify OneLogin username'
        )

        self.add_argument(
            '-d', '--duration-seconds', type=int,
            dest='duration_seconds',
            action=EnvDefault, required=False,
            help='Specify duration seconds which depend on IAM role session '
                 'duration: https://aws.amazon.com/about-aws/whats-new/2018'
                 '/03/longer-role-sessions/'
        )

        self.add_argument(
            '--reset-password', dest='reset_password', action='store_true',
            help='Prompt the user for password even if the password is '
                 'stored in the OS keychain.', default=False,
        )

        version = pkg_resources.get_distribution(__package__).version
        self.add_argument(
            '-v', '--version', action='version',
            version="%(prog)s " + version
        )

        self.add_argument(
            '-c', '--configure', dest='configure', action='store_true',
            help='Configure OneLogin and AWS settings', default=False
        )


class EnvDefault(argparse.Action):
    """Allow argparse values to be pulled from environment variables"""

    def __init__(self, required=True, default=None, **kwargs):

        if 'dest' in kwargs:
            name = 'ONELOGIN_AWS_CLI_' + kwargs['dest'].upper()
            # Fall back to the explicit command line default.
            default = os.environ.get(name, default)
            if 'type' in kwargs and default is not None:
                default = kwargs['type'](default)

        super().__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
