
# onelogin-aws-cli

A CLI utility that helps with using AWS CLI
when using AWS Roles and OneLogin authentication.

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




## Usage

Running `onelogin-aws-login`  will perform the authentication against OneLogin,
and cache the credentials in the AWS CLI Shared Credentials File.

For every required piece of information, the program will present interactive
inputs, unless that value has already been provided through either
[command line parameters](#command-line-parameters),
[environment variables](#environment-variables),
or [configuration file directives](#configuration-file).

```shell
$ onelogin-aws-login
Onelogin Username: myuser@mycompany.com
Onelogin Password:
Google Authenticator Token: 579114
Pick a role:
[1]: arn:aws:iam::166878887401:role/onelogin-test-ec2
[2]: arn:aws:iam::166878887401:role/onelogin-test-s3
[3]: arn:aws:iam::772123451421:role/onelogin-test-s3
? 3
Credentials cached in '/Users/myuser/.aws/credentials'
Expires at 2018-05-24 15:15:41+00:00
Use aws cli with --profile 772123451421:role/onelogin-test-s3/myuser@mycompany.com
```

### Interactive Configuration

Passing the `-c` or `--configure` command line parameter will start an
interactive configuration, that presents a series of interactive inputs to
gather the required pieces of information,
and save them to the [configuration file](#configuration-file) automatically.

```shell
$ onelogin-aws-login -c
```

This is a special mode of operation for this program,
and it is typically only used once, after installing the program.

However, note that it only supports a basic use case.
More advanced use cases will require manual editing of the configuration file.

### Command Line Parameters

- `-c`, `--configure` - Start interactive configuration.
- `--reset-password` - Forces a prompt for the user to re-enter their password
  even if the value is saved to the OS keychain.
- `-C`, `--config-name` - Config section to use.
- `--profile` - See the corresponding directive in the
  [configuration file](#configuration-file).
- `-u`, `--username` - See the corresponding directive in the
  [configuration file](#configuration-file).
- `-d`, `--duration-seconds` - See the corresponding directive in the
  [configuration file](#configuration-file).
- `-v`, `--version` - Print the currently installed version.

### Environment Variables

- `AWS_SHARED_CREDENTIALS_FILE` - Location of the AWS credentials file
  to write credentials to.  
  See [AWS CLI Environment Variables][aws-cli-environment-variables]
  for more information.
- `ONELOGIN_AWS_CLI_CONFIG_NAME` - Config section to use.
- `ONELOGIN_AWS_CLI_DEBUG` - Turn on debug mode.
- `ONELOGIN_AWS_CLI_PROFILE` - See the corresponding directive in the
  [configuration file](#configuration-file).
- `ONELOGIN_AWS_CLI_USERNAME` - See the corresponding directive in the
  [configuration file](#configuration-file).
- `ONELOGIN_AWS_CLI_DURATION_SECONDS` - See the corresponding directive in the
  [configuration file](#configuration-file).



## Configuration File

The configuration file is located at `~/.onelogin-aws.config`.  

It is an `.ini` file where each section defines a config name,
which can be provided using either the command line parameter `--config-name`
or the environment variable `ONELOGIN_AWS_CLI_CONFIG_NAME`.

If no config name is provided, the `[defaults]` section is used automatically.

All other sections automatically inherit from the `[defaults]` section,
and can define any additional directives as desired.

### Directives

- `base_uri` - OneLogin API base URI.  
  One of either `https://api.us.onelogin.com/`,
  or `https://api.eu.onelogin.com/` depending on your OneLogin account.
- `subdomain` - The subdomain you authenticate against in OneLogin.  
  This will be the first part of your onelogin domain.
  Eg, In `http://my_company.onelogin.com`, `my_company` would be the subdomain.
- `username` - Username to be used to authenticate against OneLogin with.  
  Can also be set with the environment variable `ONELOGIN_AWS_CLI_USERNAME`.
- `client_id` - Client ID for the user to use to authenticate against the
  OneLogin api.  
  See [Working with API Credentials][onelogin-working-with-api-credentials]
  for more details.
- `client_secret` - Client Secret for the user to use to authenticate against
  the OneLogin api.  
  See [Working with API Credentials][onelogin-working-with-api-credentials]
  for more details.
- `save_password` - Flag indicating whether `onlogin-aws-cli` can save the
  onelogin password to an OS keychain.  
  This functionality supports all keychains supported by
  [keyring][keyring-pypi].
- `profile` - AWS CLI profile to store credentials in.  
  This refers to an AWS CLI profile name defined in your `~/.aws/config` file.
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
- `ip_address` - The client IP address to send to OneLogin.
  Relevant when using OneLogin Policies with an IP whitelist.
  If this is specified, `auto_determine_ip_address` is not used.
- `auto_determine_ip_address` - Automatically determine the client IP address.
  Relevant when using OneLogin Policies with an IP whitelist.
  Can be used without specifying `ip_address`.

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
auto_determine_ip_address = yes

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



## Developing onelogin-aws-cli

#### Run tests

```shell
$ python setup.py nosetests
```



[onelogin-configuring-saml-for-aws]: https://support.onelogin.com/hc/en-us/articles/201174164-Configuring-SAML-for-Amazon-Web-Services-AWS-Single-Role
[onelogin-working-with-api-credentials]: https://developers.onelogin.com/api-docs/1/getting-started/working-with-api-credentials
[aws-cli-environment-variables]: https://docs.aws.amazon.com/cli/latest/userguide/cli-environment.html
[pyenv-github]: https://github.com/pyenv/pyenv
[keyring-pypi]: https://pypi.python.org/pypi/keyring
