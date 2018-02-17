import configparser

from onelogin_aws_cli.userquery import user_choice


class ConfigurationFile(configparser.ConfigParser):
    def __init__(self, config_file):
        super().__init__(default_section='defaults')

        self.file = config_file

        self.read_file(self.file)

    def initialise(self):
        print("Configure Onelogin and AWS\n\n")
        default = self.get_config("default")

        default["base_uri"] = user_choice("Pick a Onelogin API server:", [
            "https://api.us.onelogin.com/",
            "https://api.eu.onelogin.com/"
        ])

        print("\nOnelogin API credentials. These can be found at:\n"
              "https://admin.us.onelogin.com/api_credentials")
        default["client_id"] = input("Onelogin API Client ID: ")
        default["client_secret"] = input("Onelogin API Client Secret: ")
        print("\nOnelogin AWS App ID. This can be found at:\n"
              "https://admin.us.onelogin.com/apps")
        default["aws_app_id"] = input("Onelogin App ID for AWS: ")
        print("\nOnelogin subdomain is 'company' for login domain of "
              "'comany.onelogin.com'")
        default["subdomain"] = input("Onelogin subdomain: ")

        self.save()

    def save(self):
        with open(self.file_path, "w") as config_file:
            self.write(config_file)
        print("Configuration written to '{}'".format(self.file_path))

    def section(self, section_name):
        if self.has_section(section_name):
            return Section(section_name, self)
        return None


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

    def __getattr__(self, item):
        if self.config.has_option(self.section_name, item):
            return self.config.get(self.section_name, item)
        return None
