# onelogin-aws-cli-assume-role
Assume an AWS Role and cache credentials using Onelogin

[![Build Status](https://travis-ci.org/physera/onelogin-aws-cli.svg?branch=master)](https://travis-ci.org/healthcoda/onelogin-aws-cli)

This package provides a script to login to Onelogin and use a SAML connection
to AWS to assume a role. More details on setting up SAML for AWS can be found
at [Onelogin](https://support.onelogin.com/hc/en-us/articles/201174164-Configuring-SAML-for-Amazon-Web-Services-AWS-Single-Role).

To install, use pip

```shell
pip install onelogin-aws-cli
```

To configure the script, simply run the configuration:

```shell
onelogin-aws-login -c
```
Once installed and configured, just run onelogin-aws-login and you'll be asked for your credentials and to choose which role you want to assume.

```shell
$ onelogin-aws-login
Onelogin Username: myuser@mycompany.com
Onelogin Password:
OTP Token: 579114

Please choose the role you would like to assume:
[ 0 ]:  arn:aws:iam::166878887401:role/onelogin-test-ec2
[ 1 ]:  arn:aws:iam::166878887401:role/onelogin-test-s3
[ 2 ]:  arn:aws:iam::772123451421:role/onelogin-test-s3
Selection:
2
Credentials cached in '/Users/myuser/.aws/credentials'
Use aws cli with --profile 772123451421:role/onelogin-test-s3/myuser@mycompany.com
```
Note that `onelogin-aws-cli` requires python 3.
