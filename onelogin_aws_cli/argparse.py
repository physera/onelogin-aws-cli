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

        env_config_name = os.getenv('ONELOGIN_AWS_CLI_CONFIG_NAME')
        if env_config_name is not None:
            default_config_name = env_config_name
        else:
            default_config_name = 'default'

        self.add_argument(
            '-C', '--config-name',
            default=default_config_name,
            dest='config_name',
            help='Switch configuration name within config file'
        )

        env_profile = os.getenv('ONELOGIN_AWS_CLI_PROFILE')
        if env_profile is not None:
            default_profile = env_profile
        else:
            default_profile = ''

        self.add_argument(
            '--profile',
            default=default_profile,
            help='Specify profile name of credential',
        )

        env_username = os.getenv('ONELOGIN_AWS_CLI_USERNAME')
        if env_username is not None:
            default_username = env_username
        else:
            default_username = ''

        self.add_argument(
            '-u', '--username',
            default=default_username,
            help='Specify OneLogin username'
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
