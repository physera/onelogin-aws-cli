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
 - `ONELOGIN_AWS_CLI_CONFIG_NAME` - `onelogin-aws-cli` config section to use
 - `ONELOGIN_AWS_CLI_PROFILE` - Inject the credentials into an section with
 this title.
 - `ONELOGIN_AWS_CLI_USERNAME` - Username to be used to authenticate against
 OneLogin with.
 - `ONELOGIN_AWS_CLI_DURATION_SECONDS` - Length of the IAM STS Session in
 seconds.
 - `ONELOGIN_AWS_CLI_RENEW_SECONDS` - How often to re-authenticate the session
 in seconds.
 
## Configuration File

The configuration file is an `.ini` file with each section referring to a 
OneLogin AWS application which can be authenticated against. There is also a 
special section called `[defaults]` which has values to be used as defaults in
other sections.

### Directives

 - `base_uri` - one of either `https://api.us.onelogin.com/` or `https://api.eu.onelogin.com/`
 depending on your OneLogin account.
 - `subdomain` - the subdomain you authenticate against in OneLogin. This will
 be the first part of your onelogin domain. Eg, In `http://my_company.onelogin.com`,
 `my_company` would be the subdomain.
 - `username` - Username to be used to authenticate against OneLogin with. Can
 also be set with the environment variable `ONELOGIN_AWS_CLI_USERNAME`.
 - `save_password`  - Flag indicating whether `onlogin-aws-cli` can save the
 onelogin password to an OS keychain. This functionality supports all keychains
 supported by [keyring](https://pypi.python.org/pypi/keyring).
 - `client_id` - Client ID for the user to use to authenticate against the 
 OneLogin api. See [Working with API Credentials](https://developers.onelogin.com/api-docs/1/getting-started/working-with-api-credentials)
 for more details.
 - `client_secret` - Client Secret for the user to use to authenticate against
  the OneLogin api. See [Working with API Credentials](https://developers.onelogin.com/api-docs/1/getting-started/working-with-api-credentials)
 for more details.

### Example

```ini
[defaults]
base_uri = https://api.us.onelogin.com/
subdomain = mycompany
username = john@mycompany.com
save_password = yes
client_id = f99ee51f00400649280db1028ffa3ca9b21b680f2189b238d342cc8158c401c7
client_secret = a85234b6db01a29a493e2422d7930dffe6f4d3a826270a18838574f6b8ef7c3e

[testing]
aws_app_id = 555029

[staging]
aws_app_id = 555045

[live]
aws_app_id = 555070
```

The above configuration will allow you to have 3 different OneLogin
applications which you can authenticate against with SAML. For example, to 
authenticate against the `staging` AWS account, you could run:

    onelogin-aws-cli -C staging
