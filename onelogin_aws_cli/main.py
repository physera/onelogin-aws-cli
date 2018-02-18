#!/usr/bin/env python3

import argparse
import sys
import time

from onelogin_aws_cli import OneloginAWS

from onelogin_aws_cli import OneloginAWS, \
    DEFAULT_CONFIG_PATH
from onelogin_aws_cli.configuration import ConfigurationFile

def main():
    parser = argparse.ArgumentParser(description="Login to AWS with Onelogin")
    parser.add_argument("-c", "--configure", dest="configure",
                        action="store_true",
                        help="Configure Onelogin and AWS settings")
    parser.add_argument("-C", "--config_name", default="default",
                        help="Switch configuration name within config file")
    parser.add_argument("--profile", default="",
                        help="Specify profile name of credential")
    parser.add_argument("-u", "--username", default="",
                        help="Specify OneLogin username")
    parser.add_argument("-r", "--renewSeconds", type=int,
                        help="Auto-renew credentials after this many seconds")

    args = parser.parse_args()

    with open(DEFAULT_CONFIG_PATH) as fp:
        configFile = ConfigurationFile(fp)

    if args.configure:
        configFile.initialise()

    config_section = configFile.section(args.config_name)

    if config_section is None:
        sys.exit("Configuration '{}' not defined. "
                 "Please run 'onelogin-aws-login -c'".format(args.config_name))

    api = OneloginAWS(config_section, args)
    api.save_credentials()

    if args.renewSeconds:
        while True:
            time.sleep(args.renewSeconds)
            api.save_credentials()

if __name__ == '__main__':
    main()
