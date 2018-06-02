"""Static User Configuration models"""
import configparser
from typing import Optional, Union

from onelogin_aws_cli.userquery import user_choice


class ConfigurationFile(configparser.ConfigParser):
    """Represents a configuration ini file on disk"""

    DEFAULTS = dict(
        save_password=False,
        reset_password=False,
        duration_seconds=3600
    )

    REQUIRED = [
        'base_uri',
        'client_id',
        'client_secret',
        'aws_app_id',
        'subdomain',
    ]

    def __init__(self, config_file=None):
        super().__init__(
            default_section='defaults',
        )

        self.file = config_file

        if self.file is not None:
            self.load()

    @property
    def has_defaults(self) -> bool:
        """True if the default section is non-empty"""
        return len(self.items(self.default_section)) > 0

    @property
    def is_initialised(self) -> bool:
        """True if there is at least one section"""
        return (len(self.sections()) > 0) or self.has_defaults

    def load(self):
        self.read_file(self.file)

    def initialise(self, config_name='defaults'):
        """
        Prompt the user for configurations, and save them to the
        onelogin-aws-cli config file
        """
        print("Configure Onelogin and AWS\n\n")
        config_section = self.section(config_name)
        if config_section is None:
            self.add_section(config_name)
            config_section = self.section(config_name)

        config_section['base_uri'] = user_choice(
            "Pick a Onelogin API server:", [
                "https://api.us.onelogin.com/",
                "https://api.eu.onelogin.com/"
            ]
        )

        print("\nOnelogin API credentials. These can be found at:\n"
              "https://admin.us.onelogin.com/api_credentials")
        config_section['client_id'] = input("Onelogin API Client ID: ")
        config_section['client_secret'] = input("Onelogin API Client Secret: ")
        print("\nOnelogin AWS App ID. This can be found at:\n"
              "https://admin.us.onelogin.com/apps")
        config_section['aws_app_id'] = input("Onelogin App ID for AWS: ")
        print("\nOnelogin subdomain is 'company' for login domain of "
              "'comany.onelogin.com'")
        config_section['subdomain'] = input("Onelogin subdomain: ")

        self.save()

    def save(self):
        """Save this config to disk"""
        self.write(self.file)
        print("Configuration written to '{}'".format(
            self.file.name if hasattr(self.file, 'name') else self.file,
        ))

    def section(self, section_name: str):
        """
        Return a Section object representing a single section within the
        onelogin config file.

        :param section_name: Name of the section in the config file
        :return:
        """
        section_missing = not self.has_section(section_name)
        not_default = self.default_section != section_name
        if section_missing and not_default:
            return None
        return Section(section_name, self)


class Section(object):
    """Represents a single section in an ini file"""

    def __init__(self, section_name: str, config: ConfigurationFile):
        self.config = config
        self.section_name = section_name
        self._overrides = {}

        self._cast_handler_mappings = {
            'can_': lambda i: self.config.getboolean(
                self.section_name, i, fallback=False
            ),
        }

    def _get_has_required(self) -> bool:
        """
        Returns true if the section (including the defaults fallback)
        contains all the required keys.
        """
        return all([
            self.__contains__(item) for item in ConfigurationFile.REQUIRED
        ])

    def set_overrides(self, overrides: dict):
        """
        Specify a dictionary values which take precedence over the existing
        values, but will not overwrite them in the config file.
        :param overrides:
        """
        self._overrides = {k: v for k, v in overrides.items() if v is not None}

    def _has_cast_handler(self, item) -> bool:
        """
        Checks if the property has a format assuming it has a cast handler

        If an attribute starts with `can_` it will be assumed to be cast as
        boolean, and the key will be item with `can_` removed from the
        suffix.

        :param item:
        :return:
        """

        return any([item.startswith(prefix)
                    for prefix in self._cast_handler_mappings.keys()])

    def _cast_handler(self, item) -> Optional[bool]:
        """Casts the item from string to a type"""

        for prefix, handler in self._cast_handler_mappings.items():
            if item.startswith(prefix):
                return handler(item[len(prefix):])

    def __setitem__(self, key, value):
        self.config.set(self.section_name, key, value)

    def __getitem__(self, item) -> Optional[Union[str, bool]]:
        """
        Single location to handle the precedence of configurations.
        The precedence chain is:
          - overrides
          - configuration functions
          - config files/cli options/environment variables
          - class level defaults

        :param item: name of the configuration to get.
        :return:
        """

        raw_item = item
        for prefix in self._cast_handler_mappings.keys():
            raw_item = item[item.startswith(prefix) and len(prefix):]

        # Is it in the overrides
        if raw_item in self._overrides:
            return self._overrides[raw_item]

        # Do we have a private handler function?
        if self._has_cast_handler(item):
            return self._cast_handler(item)

        func = "_get_" + item
        if hasattr(self, func) and callable(getattr(self, func)):
            return getattr(self, func)()

        # Is it in the configuration?
        if self.config.has_option(self.section_name, raw_item):
            return self.config.get(self.section_name, raw_item)

        # Is it in the class level defaults?
        return self.config.DEFAULTS[raw_item]

    def __contains__(self, item):
        func = "_get_" + item
        for prefix in self._cast_handler_mappings.keys():
            raw_item = item[item.startswith(prefix) and len(prefix):]

        has_item_defined = self.config.has_option(self.section_name, raw_item)
        has_handler = hasattr(self, func) and callable(getattr(self, func))
        has_cast_handler = self._has_cast_handler(item)
        has_default_value = raw_item in self.config.DEFAULTS

        return has_item_defined or \
            has_handler or \
            has_cast_handler or \
            has_default_value

    def get(self, item, default=None):
        if self.__contains__(item):
            return self.__getitem__(item)
        return default
