
# onelogin-aws-cli

A CLI utility that helps with using AWS CLI when using AWS Roles and OneLogin authentication.

[![Build Status](https://travis-ci.org/physera/onelogin-aws-cli.svg?branch=master)](https://travis-ci.org/physera/onelogin-aws-cli)
[![codecov](https://codecov.io/gh/physera/onelogin-aws-cli/branch/master/graph/badge.svg)](https://codecov.io/gh/physera/onelogin-aws-cli)


This package provides a CLI utility program that:

- Authenticates against OneLogin.
- Fetches a list of available Roles in AWS for a given OneLogin AWS App.
- Allows the user to select a Role to assume.
- Saves credentials for the assumed role in the AWS CLI Shared Credentials File.

In order to be able to use this program, you must first
[Configure SAML for AWS in OneLogin][onelogin-configuring-saml-for-aws].

Note that while the repo and the pip package are called `onelogin-aws-cli`,
the installed program is called `onelogin-aws-login`.



## Installation

To install, use pip:

```shell
$ pip install onelogin-aws-cli
```

Note that `onelogin-aws-cli` requires Python 3.

Note that it is not recommended to install Python packages globally
on your system.
[Pyenv][pyenv-github] is a great tool for managing your Python environments.



## Interactive configuration

To configure the script, simply run the configuration:

```shell
$ onelogin-aws-login -c
```
Once installed and configured, just run `onelogin-aws-login` and you'll be asked for your credentials and to choose which role you want to assume.

```shell
$ onelogin-aws-login
Onelogin Username: myuser@mycompany.com
Onelogin Password:
Google Authenticator Token: 579114
Pick a role:
[0]: arn:aws:iam::166878887401:role/onelogin-test-ec2
[1]: arn:aws:iam::166878887401:role/onelogin-test-s3
[2]: arn:aws:iam::772123451421:role/onelogin-test-s3
? 2
Credentials cached in '/Users/myuser/.aws/credentials'
Expires at 2018-05-24 15:15:41+00:00
Use aws cli with --profile 772123451421:role/onelogin-test-s3/myuser@mycompany.com
```


## Usage

There are two mode of operation for the utility: configure and log in. Specify
the option `--configure` to enable the configuration of the utility and omit it
to use the log in functionality

### CLI Options

 - `--configure` - Starts an interactive session which will prompt the user for
        values to fill out a configuration.
 - `--reset-password` - Forces a prompt for the user to re-enter their password
        even if the value is saved to the OS keychain.


## Environment Variables

- `AWS_SHARED_CREDENTIALS_FILE` - Location of the AWS credentials file
  to write credentials to.  
  See [AWS CLI Environment Variables](aws-cli-environment-variables)
  for more information.
- `ONELOGIN_AWS_CLI_CONFIG_NAME` - `onelogin-aws-cli` config section to use.
- `ONELOGIN_AWS_CLI_DEBUG` - Turn on debug mode.
- `ONELOGIN_AWS_CLI_PROFILE` - See the corresponding value in the
  [configuration file](#configuration-file).
- `ONELOGIN_AWS_CLI_USERNAME` - See the corresponding value in the
  [configuration file](#configuration-file).
- `ONELOGIN_AWS_CLI_DURATION_SECONDS` - See the corresponding value in the
  [configuration file](#configuration-file).


## Configuration File

The configuration file is an `.ini` file with each section referring to a
OneLogin AWS application which can be authenticated against. There is also a
special section called `[defaults]` which has values to be used as defaults in
other sections.

### Directives

- `base_uri` - One of either `https://api.us.onelogin.com/` or `https://api.eu.onelogin.com/`
  depending on your OneLogin account.
- `subdomain` - The subdomain you authenticate against in OneLogin.  
  This will be the first part of your onelogin domain.
  Eg, In `http://my_company.onelogin.com`, `my_company` would be the subdomain.
- `username` - Username to be used to authenticate against OneLogin with.  
  Can also be set with the environment variable `ONELOGIN_AWS_CLI_USERNAME`.
  This functionality supports all keychains supported by
  [keyring](https://pypi.python.org/pypi/keyring).
- `client_id` - Client ID for the user to use to authenticate against the
  OneLogin api.  
  See [Working with API Credentials](https://developers.onelogin.com/api-docs/1/getting-started/working-with-api-credentials)
  for more details.
- `client_secret` - Client Secret for the user to use to authenticate against
  the OneLogin api.  
  See [Working with API Credentials](https://developers.onelogin.com/api-docs/1/getting-started/working-with-api-credentials)
  for more details.
- `save_password` - Flag indicating whether `onlogin-aws-cli` can save the
  onelogin password to an OS keychain.
- `profile` - AWS CLI profile to store credentials in.  
  This refers to an AWS CLI profile name defined in your `~./aws/config` file.
- `duration_seconds` - Length of the IAM STS session in seconds.  
  This cannot exceed the maximum duration specified in AWS for the given role.
- `aws_app_id` - ID of the AWS App instance in your OneLogin account.
  This ID can be found by logging in to your OneLogin web dashboard
  and navigating to `Administration` -> `APPS` -> `<Your app instance>`,
  and copying it from the URL in the address bar.
- `role_arn` - AWS Role ARN to assume after authenticating against OneLogin.  
  Specifying this will disable the display of available roles and the
  interactive choice to select a role after authenticating.
- `otp_device` - Allow the automatic selection of an OTP device.  
  This value is the human readable string name for the device.
  Eg, `OneLogin Protect`, `Yubico YubiKey`, etc

### Example

```ini
[defaults]
base_uri = https://api.us.onelogin.com/
subdomain = mycompany
username = john@mycompany.com
client_id = f99ee51f00400649280db1028ffa3ca9b21b680f2189b238d342cc8158c401c7
client_secret = a85234b6db01a29a493e2422d7930dffe6f4d3a826270a18838574f6b8ef7c3e
save_password = yes
profile = mycompany-onelogin
duration_seconds = 3600

[testing]
aws_app_id = 555029

[staging]
aws_app_id = 555045

[live]
aws_app_id = 555070

[testing-admin]
aws_app_id = 555029
role_arn = arn:aws:iam::123456789123:role/Admin

[staging-admin]
aws_app_id = 555045
role_arn = arn:aws:iam::123456789123:role/Admin

[live-admin]
aws_app_id = 555070
role_arn = arn:aws:iam::123456789123:role/Admin
```

This example will let you select from 6 config names,
that are variations of the same base values specified in `[defaults]`.

The first three, `testing`, `staging`, and `live`,
all have different OneLogin application IDs.

The latter three, `testing-admin`, `staging-admin`, and `live-admin`,
also have `role_arn` specified,
so they will automatically assume the role with that ARN.

For example, to use the `staging` config, you could run:

```shell
$ onelogin-aws-login -C staging
```

And to use the `live-admin` config, you could run:

```shell
$ onelogin-aws-login -C live-admin
```



[onelogin-configuring-saml-for-aws]: https://support.onelogin.com/hc/en-us/articles/201174164-Configuring-SAML-for-Amazon-Web-Services-AWS-Single-Role
[aws-cli-environment-variables]: https://docs.aws.amazon.com/cli/latest/userguide/cli-environment.html
[pyenv-github]: https://github.com/pyenv/pyenv
