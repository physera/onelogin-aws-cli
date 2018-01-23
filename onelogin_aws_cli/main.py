#!/usr/bin/env python3

import argparse
import sys
import time

from onelogin_aws_cli import OneloginAWS


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

    if args.configure:
        OneloginAWS.generate_config()

    config = OneloginAWS.load_config()

    if not config or args.config_name not in config:
        sys.exit("Configuration '{}' not defined. "
                 "Please run 'onelogin-aws-login -c'".format(args.config_name))

    api = OneloginAWS(config[args.config_name], args)
    api.save_credentials()

    if args.renewSeconds:
        while True:
            time.sleep(args.renewSeconds)
            api.save_credentials()


if __name__ == '__main__':
    main()
