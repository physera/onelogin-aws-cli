"""
CLI Argument Parser
"""

import argparse

import pkg_resources


class OneLoginAWSArgumentParser(argparse.ArgumentParser):
    """
    Argument Parser separated into daemon and cli tool
    """

    def __init__(self):
        super().__init__(description='Login to AWS with OneLogin')

        version = pkg_resources.get_distribution('pip').version
        self.add_argument(
            '-v', '--version', action='version',
            version='%(prog)s ' + version
        )

        self.add_argument(
            '-C', '--config-name', default='default', dest='config_name',
            help='Switch configuration name within config file'
        )

        self.add_argument(
            '--profile', default='', help='Specify profile name of credential'
        )

        self.add_argument(
            '-u', '--username', default='', help='Specify OneLogin username'
        )

    def add_cli_options(self):
        """
        Add Argument Parser options only used in the CLI entrypoint
        """

        self.add_argument(
            '-r', '--renew-seconds', type=int,
            help='Auto-renew credentials after this many seconds'
        )

        self.add_argument(
            '-c', '--configure', dest='configure', action='store_true',
            help='Configure OneLogin and AWS settings'
        )

        version = pkg_resources.get_distribution('pip').version
        self.add_argument(
            '-v', '--version', action='version', version='%(prog)s ' + version
        )

        # The `--client` option is a precursor to the daemon process in
        # https://github.com/physera/onelogin-aws-cli/issues/36
        # self.add_argument("--client", dest="client_mode",
        #                   action='store_true')

        return self
