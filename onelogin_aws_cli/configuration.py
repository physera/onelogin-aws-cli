import configparser

from onelogin_aws_cli.userquery import user_choice


class ConfigurationFile(configparser.ConfigParser):
    def __init__(self, config_file):
        super().__init__(default_section='defaults')

        self.file = config_file

        self.read_file(self.file)

    def initialise(self):
        print("Configure Onelogin and AWS\n\n")
        default = self.section("default")

        default['base_uri'] = user_choice("Pick a Onelogin API server:", [
            "https://api.us.onelogin.com/",
            "https://api.eu.onelogin.com/"
        ])

        print("\nOnelogin API credentials. These can be found at:\n"
              "https://admin.us.onelogin.com/api_credentials")
        default['client_id'] = input("Onelogin API Client ID: ")
        default['client_secret'] = input("Onelogin API Client Secret: ")
        print("\nOnelogin AWS App ID. This can be found at:\n"
              "https://admin.us.onelogin.com/apps")
        default['aws_app_id'] = input("Onelogin App ID for AWS: ")
        print("\nOnelogin subdomain is 'company' for login domain of "
              "'comany.onelogin.com'")
        default['subdomain'] = input("Onelogin subdomain: ")

        self.save()

    def save(self):
        self.write(self.file)
        print("Configuration written to '{}'".format(self.file))

    def section(self, section_name):
        if not self.has_section(section_name):
            self.add_section(section_name)
        return Section(section_name, self)


class Section(object):
    def __init__(self, section_name, config: ConfigurationFile):
        self.config = config
        self.section_name = section_name

    @property
    def can_save_password(self) -> bool:
        return self.config.getboolean(self.section_name, "save_password")

    @property
    def can_save_username(self) -> bool:
        return self.config.getboolean(self.section_name, "save_username")

    def __setitem__(self, key, value):
        self.config.set(self.section_name, key, value)

    def __getitem__(self, item):
        self.config.get(self.section_name, item)
