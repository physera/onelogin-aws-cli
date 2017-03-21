# onelogin-aws-cli-assume-role
Assume an AWS Role and cache credentials using Onelogin

[![Build Status](https://travis-ci.org/healthcoda/onelogin-aws-cli.svg?branch=master)](https://travis-ci.org/healthcoda/onelogin-aws-cli)

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