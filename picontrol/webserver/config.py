#!/usr/bin/python 
# config.py

from typing import Optional
from configparser import ConfigParser


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
        self.update_version = self.load_update_version()
        self.theme = self.config.get("user", "theme")
        self.user = self.get_user()
        self.fan_settings = self.get_fan_settings()
        self.button_settings = self.get_button_settings()
        self.pi_version = self.get_pi_model()

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

    def get_user(self):
        """
        Get the user from the config file
        """
        return {
            "username": self.config.get("user", "username"),
            "password": self.config.get("user", "password"),
        }

    def get_fan_settings(self):
        """
        Get the fan settings from the config file
        """
        return {
            "thresholdOn": self.config.get("fan", "thresholdOn"),
            "thresholdOff": self.config.get("fan", "thresholdOff"),
            "interval": self.config.get("fan", "interval"),
        }

    def get_button_settings(self):
        """
        Get the button settings from the config file
        """
        return self.config.get("button", "option")

    @staticmethod
    def get_pi_model():
        """
        Determine the Raspberry Pi model from the device-tree model file

        :return: Raspberry Pi model number, if available
        :rtype: Optional[int]
        """
        with open('/proc/device-tree/model', 'r') as file:
            data = file.read()
        import re
        numbers = re.findall(r'[0-9]+', data)
        if numbers:
            return numbers[0]
        return None
