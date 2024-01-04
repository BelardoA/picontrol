#!/usr/bin/python 
#config.py

import ConfigParser


class Config:
    """
    Config class to load and save config files from disk
    """

    def __init__(self):
        self.base_path = '/home/pi/scripts/picontrol/configs'
        self.update_path = '/home/pi/scripts/picontrol_update/picontrol/configs'
        self.config_file = 'config.conf'
        self.version_file = 'picontrol.version'
        self.config_parser = ConfigParser.RawConfigParser()
        self.config = self.load_config()
        self.version = self.load_version()

    def load_config(self):
        """
        Load the config file from disk (config.conf)
        """
        return self.config_parser.read(self.base_path + self.config_file)

    def save_config(self, config):
        """
        Save the config file to disk (config.conf)
        """
        with open(self.base_path + self.config_file, 'w') as out_file:
            config.write(out_file)
        return True

    def load_version(self):
        """
        Load the version file from disk (picontrol.version)
        """
        return self.config_parser.read(self.base_path + self.version_file)

    def save_version(self, config):
        """
        Save the version file to disk (picontrol.version)
        """
        with open(self.base_path + self.version_file, 'w') as out_file:
            config.write(out_file)
        return True

    def load_update_version(self):
        """
        Load the update version file from disk
        """
        return self.config_parser.read(self.update_path + self.version_file)
