import getpass
import typing

import keyring

from onelogin_aws_cli.configuration import Section


class UserCredentials(object):
    SERVICE_NAME = "onelogin-aws-cli"

    def __init__(self, username, config: Section):
        self.username = username
        self.password = None
        self.configuration = config

    def load_credentials(self):
        save_password = False

        if not self.username:
            # Try the configuration first
            if 'username' in self.configuration:
                self.username = self.configuration['username']
            else:
                self.username = input("Onelogin Username: ")

        if not self.password:
            if self.configuration.can_save_password:
                self.password = self.load_password_from_keychain()
                if self.password is None:
                    save_password = True
                    self.prompt_password()
            else:
                self.prompt_password()

        if save_password:
            print("Saving password to keychain...")
            self.save_password_to_keychain()

    def prompt_password(self):
        self.password = getpass.getpass("Onelogin Password: ")

    def load_password_from_keychain(self) -> typing.Union[str, bool]:
        return keyring.get_password(self.SERVICE_NAME, self.username)

    def save_password_to_keychain(self):
        keyring.set_password(self.SERVICE_NAME, self.username, self.password)
