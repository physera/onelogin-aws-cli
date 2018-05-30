from io import StringIO

from onelogin_aws_cli.configuration import ConfigurationFile


def build_config(config_content: str):
    str = StringIO()
    str.write(config_content)
    str.seek(0)
    return ConfigurationFile(str)
