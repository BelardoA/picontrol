#!/usr/bin/python 
# config.py

import json
import os
from typing import Optional


class Config:
    """
    Config class to load and save config files from disk as well as provide default values for missing keys.
    """

    def __init__(self):
        self.template = {
            "user": {
                "username": "picontrol",
                "password": "password",
                "theme": "default"
            },
            "fan": {
                "thresholdOn": 65,
                "thresholdOff": 55,
                "interval": 5
            },
            "button": {
                "option": 1
            }
        }
        # self.update_version = self.parse_config(self.update_path + self.version_file)
        self.update_path = '/home/pi/scripts/picontrol_update/picontrol/configs'
        # self.config_file = '/home/pi/scripts/picontrol/configs/config.json'
        self.config_file = f'{os.getcwd()}/configs/config.json'
        self.config = self.get_config()
        self.version = self.config["version"]["number"]
        self.user = self.config["user"]
        self.site_settings = self.config["site"]
        self.fan_settings = self.config["fan"]
        self.button_settings = self.config["button"]["option"]
        self.pi_version = self.get_pi_model()

    def verify_config(self, template, config) -> dict:
        """
        Verify keys and value types in init.yaml while retaining keys in config that are not present in template.

        :param dict template: Default template configuration.
        :param dict config: Dictionary to compare against template.
        :return: validated and/or updated config.
        :rtype: dict
        """
        updated_config = config.copy()  # Start with a copy of the original config

        # Update or add template keys in config
        for key, template_value in template.items():
            config_value = config.get(key)

            # If key missing or value type mismatch, use template value
            if (
                config_value is None
                or config_value == ""
                or not isinstance(config_value, type(template_value))
            ):
                updated_config[key] = template_value
            # If value is a dict, recurse
            elif isinstance(template_value, dict):
                updated_config[key] = self.verify_config(
                    template_value, config.get(key, {})
                )
            # Else, retain the config value
            else:
                updated_config[key] = config_value

        return updated_config

    def get_config(self) -> dict:
        """
        Verify the config file exists and has the correct structure.

        :return: validated and/or updated config.
        :rtype: dict
        """
        if not os.path.exists(self.config_file):
            print("Config file not found, creating...")
            with open(self.config_file, 'w') as out_file:
                json.dump(self.template, out_file, indent=4)
                config = self.template
        else:
            print("Config file found, verifying...")
            with open(self.config_file, 'r') as file:
                config = json.load(file)
            config = self.verify_config(self.template, config)
            with open(self.config_file, 'w') as out_file:
                json.dump(config, out_file, indent=4)
        return config

    def save_config(self, config: dict) -> bool:
        """
        Save the config file to disk (config.conf)

        :param dict config: Dictionary to save to disk.
        :return: True if successful, False otherwise.
        """
        with open(self.config_file, 'w') as out_file:
            json.dump(config, out_file, indent=4)
            self.config = config
        return os.path.exists(self.config_file)

    @staticmethod
    def get_pi_model() -> Optional[int]:
        """
        Determine the Raspberry Pi model from the device-tree model file

        :return: Raspberry Pi model number, if available
        :rtype: Optional[int]
        """
        try:
            with open('/proc/device-tree/model', 'r') as file:
                data = file.read()
            import re
            if numbers := re.findall(r'[0-9]+', data):
                return numbers[0]
        except FileNotFoundError:
            return None
        return None
