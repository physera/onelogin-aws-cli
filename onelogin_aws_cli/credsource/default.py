"""
CLI credentials source. Will prompt the user.
"""

from onelogin_aws_cli.credsource import CredentialsSource


class DefaultCredentialsSource(CredentialsSource):
    """
    A credentials source which throws an exception for all cred sources.
    Used as a base for the credentials chain. Will primarily be used
    for the daemo.
    """
    pass
