"""
Handles the saving and loading of username and password in a secure
manner
"""
import getpass

import keyring

from onelogin_aws_cli.configuration import Section


class UserCredentials(object):
    """
    Class to encapsulate the handling of storing and retrieving user password
    in OS-Independent system keychain.
    """
    SERVICE_NAME = "onelogin-aws-cli"

    def __init__(self, username, config: Section):
        self.username = username
        self.configuration = config

        # This is `None`, as the password should be be emitted from this class
        # and should never be loaded from any other source outside this class
        self.password = None

        self._interactive = True

    @property
    def has_password(self) -> bool:
        """
        True if the class has a password.

        :return:Whether we have set a password or not, yet
        """
        return (self.password is not None) and \
               (self.password != "")

    def disable_interactive(self):
        """
        Disable all user prompts. In the event there is missing data,
        an exception will be thrown in place of a user prompt.

        :return:
        """
        self._interactive = False

    def load_credentials(self):
        """
        Load the username and password
        """

        self.load_username()
        self.load_password()

    def load_username(self):
        """
        Either load the username from configfile or prompt the user to supply
        one interactively

        :return: username
        """

        if not self.username:
            # Try the configurationfile first
            if 'username' in self.configuration:
                username = self.configuration['username']
            else:
                username = input("Onelogin Username: ")
            self.username = username

    def load_password(self):
        """
        Load the password from keychain if we expect to be able to save the
        password in a keychain, or prompt the user for a password through
        stdin.

        :return: user password
        """

        save_password = False

        # Do we have a password?
        if not self.has_password:
            # Can we load the password from os keychain?
            if self.configuration.can_save_password:

                # Load the password from OS keychain
                self._load_password_from_keychain()

                # Could not find password in OS keychain
                if not self.has_password:
                    # Ask user for password
                    self._prompt_user_password()
                    # Remember to save password
                    save_password = True

                if not self.has_password:
                    # We still don't have a password and have exhausted all
                    # places to load one from.
                    raise RuntimeError(
                        "Could not load password from secure store " +
                        "nor from user input"
                    )
            else:
                # Ask the user
                self._prompt_user_password()

            if save_password:
                # We decided to save the password
                print("Saving password to keychain...")
                self._save_password_to_keychain()

    def _prompt_user_password(self):
        self.password = getpass.getpass("Onelogin Password: ")

    def _load_password_from_keychain(self):
        self.password = keyring.get_password(self.SERVICE_NAME, self.username)

    def _save_password_to_keychain(self):
        keyring.set_password(self.SERVICE_NAME, self.username, self.password)
