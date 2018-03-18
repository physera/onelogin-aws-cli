"""
Collections of entrypoints
"""
import signal
import sys
from threading import Event

from onelogin_aws_cli import DEFAULT_CONFIG_PATH, OneloginAWS
from onelogin_aws_cli.argparse import OneLoginAWSArgumentParser
from onelogin_aws_cli.configuration import ConfigurationFile
from onelogin_aws_cli.model import SignalRepr


def login(args=sys.argv[1:]):
    """
    Entrypoint for `onelogin-aws-login`
    :param args:
    """

    parser = OneLoginAWSArgumentParser().add_cli_options()
    args = parser.parse_args(args)

    with open(DEFAULT_CONFIG_PATH, 'a+') as fp:
        fp.seek(0, 0)
        config_file = ConfigurationFile(fp)

    if args.configure or not config_file.is_initialised:
        config_file.initialise(args.config_name)

    config_section = config_file.section(args.config_name)

    if config_section is None:
        sys.exit("Configuration '{}' not defined. "
                 "Please run 'onelogin-aws-login -c'".format(args.config_name))

    # Handle legacy `--renewSeconds` option while it is depecated
    if args.renew_seconds:
        renew_seconds = args.renew_seconds
    elif args.renew_seconds_legacy:
        renew_seconds = args.renew_seconds_legacy
    else:
        renew_seconds = None

    api = OneloginAWS(config_section, args)
    api.save_credentials()

    if renew_seconds:

        interrupted = Event()

        def _interrupt_handler(signal_num: int, *args):
            interrupted.set()
            print("Received {sig}.".format(sig=SignalRepr(signal_num)))
            print("Shutting down Credentials refresh process...")

        # Handle sigterms
        # This must be done here, as signals can't be caught down the stack
        for sig_type in list(SignalRepr):
            signal.signal(sig_type.value, _interrupt_handler)

            # @TODO We should check if the credentials are going to expire
            # in the immediate future, rather than constantly hitting
            # the AWS API.

        interrupted.clear()
        while not interrupted.is_set():
            interrupted.wait(renew_seconds)
            api.save_credentials()
