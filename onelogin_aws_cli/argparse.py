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
            variable_name='ONELOGIN_AWS_CLI_CONFIG_NAME', action=EnvDefault,
            dest='config_name',
            help='Switch configuration name within config file'
        )

        self.add_argument(
            '--profile',
            variable_name='ONELOGIN_AWS_CLI_PROFILE', action=EnvDefault,
            help='Specify profile name of credential',
        )

        self.add_argument(
            '-u', '--username',
            variable_name='ONELOGIN_AWS_CLI_USERNAME', action=EnvDefault,
            help='Specify OneLogin username'
        )

        self.add_argument(
            '-d', '--duration-seconds', type=int, default=3600,
            dest='duration_seconds',
            help='Specify duration seconds which depend on IAM role session '
                 'duration: https://aws.amazon.com/about-aws/whats-new/2018'
                 '/03/longer-role-sessions/'
        )

        version = pkg_resources.get_distribution(__package__).version
        self.add_argument(
            '-v', '--version', action='version',
            version="%(prog)s " + version
        )

        renew_seconds_group = self.add_mutually_exclusive_group()

        renew_seconds_group.add_argument(
            '-r', '--renew-seconds', type=int,
            help='Auto-renew credentials after this many seconds'
        )

        renew_seconds_group.add_argument(
            # Help is suppressed as this is replaced by the POSIX friendlier
            # version above. This is here for legacy compliance and will
            # be deprecated.
            '--renewSeconds', type=int, help=argparse.SUPPRESS,
            dest='renew_seconds_legacy'
        )

        self.add_argument(
            '-c', '--configure', dest='configure', action='store_true',
            help='Configure OneLogin and AWS settings'
        )

        return self


class EnvDefault(argparse.Action):
    """
    Allow argparse values to be pulled from environment variables
    """

    def __init__(self, variable_name, required=True, default=None, **kwargs):
        if not default and variable_name:
            if variable_name in os.environ:
                default = os.environ[variable_name]
        if required and default:
            required = False
        super(EnvDefault, self).__init__(default=default, required=required,
                                         **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
