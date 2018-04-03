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
            default=os.getenv(
                'ONELOGIN_AWS_CLI_CONFIG_NAME',
                default='default',
            ),
            dest='config_name',
            help='Switch configuration name within config file'
        )

        self.add_argument(
            '--profile',
            default=os.getenv(
                'ONELOGIN_AWS_CLI_PROFILE',
                default='',
            ),
            help='Specify profile name of credential',
        )

        self.add_argument(
            '-u', '--username',
            default=os.getenv(
                'ONELOGIN_AWS_CLI_USERNAME',
                default='',
            ),
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

    def add_cli_options(self):
        """Add Argument Parser options only used in the CLI entrypoint"""

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

        # The `--client` option is a precursor to the daemon process in
        # https://github.com/physera/onelogin-aws-cli/issues/36
        # self.add_argument("--client", dest="client_mode",
        #                   action='store_true')

        return self
