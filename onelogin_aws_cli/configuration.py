import configparser

from onelogin_aws_cli import user_choice


class ConfigurationFile(configparser.ConfigParser):
    def __init__(self, config_file):
        super().__init__()
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

    @property
    def can_save_password(self):
        pass

    @property
    def can_save_username(self):
        pass

    def get_profile(self, name):
        if name not in self:
            return None
        return self[name]

    def get_config(self, name):
        config_name = 'config ' + name
        return self.get_profile(config_name)

    def save(self):
        with open(self.file_path, "w") as config_file:
            self.write(config_file)
        print("Configuration written to '{}'".format(self.file_path))
