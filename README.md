# onelogin-aws-cli-assume-role
Assume an AWS Role and cache credentials using Onelogin

[![Build Status](https://travis-ci.org/physera/onelogin-aws-cli.svg?branch=master)](https://travis-ci.org/physera/onelogin-aws-cli)
[![codecov](https://codecov.io/gh/physera/onelogin-aws-cli/branch/master/graph/badge.svg)](https://codecov.io/gh/physera/onelogin-aws-cli)

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

## Environment Variables

- `AWS_SHARED_CREDENTIALS_FILE` - Specifies the location of the AWS credentials
  file to write credentials out to. See
  [Environment Variables](https://docs.aws.amazon.com/cli/latest/userguide/cli-environment.html)
  for more information.
- `ONELOGIN_AWS_CLI_CONFIG_NAME` - `onelogin-aws-cli` config section to use.
- `ONELOGIN_AWS_CLI_DEBUG` - Turn on debug mode.
- `ONELOGIN_AWS_CLI_PROFILE` - See the correspondig value in the
  [configuration file](#configuration-file).
- `ONELOGIN_AWS_CLI_USERNAME` - See the correspondig value in the
  [configuration file](#configuration-file).
- `ONELOGIN_AWS_CLI_DURATION_SECONDS` - See the correspondig value in the
  [configuration file](#configuration-file).
- `ONELOGIN_AWS_CLI_RENEW_SECONDS` - See the correspondig value in the
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
- `renew_seconds` - How often to re-authenticate the session in seconds.
- `aws_app_id` - ID of the AWS App instance in your OneLogin account.  
  This ID can be found by logging in to your OneLogin web dashboard
  and navigating to `Administration` -> `APPS` -> `<Your app instance>`,
  and copying it from the URL in the address bar.
- `role_arn` - AWS Role ARN to assume after authenticating against OneLogin.  
  Specifying this will disable the display of available roles and the
  interactive choice to select a role after authenticating.

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
renew_seconds = 60

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
$ onelogin-aws-cli -C staging
```

And to use the `live-admin` config, you could run:

```shell
$ onelogin-aws-cli -C live-admin
```
