import yaml


class Config:
    """
    Module for reading all configuration information from config.yaml file.
    Make sure the config.yaml file exists and all the relevant fields are populated.
    """

    def __init__(self):
        self.project_id = None
        self.file_name = None
        self.key = None
        self.tags = None
        self.filter = None
        self.GS_CREDENTIALS = None
        self.sender_user = None
        self.recipient_user = None
        self.component_filter = None

    def load(self):
        """
        Function loads the configuration information.
        """
        with open(r"config/config.yaml", "r") as file:
            yaml_config = yaml.safe_load(file)
        self.project_id = yaml_config["project_id"]
        self.file_name = yaml_config["file_name"]
        self.key = yaml_config["key"]
        self.tags = yaml_config["tags"]
        self.filter = yaml_config["filter"]
        self.GS_CREDENTIALS = yaml_config["GS_CREDENTIALS"]
        self.sender_user = yaml_config["sender_user"]
        self.recipient_user = yaml_config["recipient_user"]
        self.component_filter = yaml_config["component_filter"]

    def view(self):
        """
        Function to display googlesheet creds.
        """
        print(self.GS_CREDENTIALS)
