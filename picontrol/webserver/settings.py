#!/usr/bin/python 
# settings.py

import os
from config import Config


class Settings:
    def __init__(self):
        self.update_dir = '/home/pi/scripts/picontrol_update'
        self.base_dir = '/home/pi/scripts/picontrol'
        self.config = Config()

    def set_fan_settings(self, fan_settings):
        """
        Set the fan settings in the config file

        :param dict fan_settings: The fan settings to save
        :return: True if the settings were saved, False otherwise
        :rtype: bool
        """
        try:
            self.config.fan_settings = {
                "thresholdOn": fan_settings['thresholdOn'],
                "thresholdOff": fan_settings['thresholdOff'],
                "interval": fan_settings['interval'],
            }
            self.config.save_config(self.config.config)
            return True
        except Exception as ex:
            print('Error saving fan settings: ' + str(ex))
            return False

    def get_fan_settings(self):
        """
        Function to get fan settings from config file

        :returns: Dictionary containing fan settings
        :rtype: dict
        """
        try:
            return self.config.fan_settings
        except Exception as ex:
            print("Error getting fanSettings from config: " + str(ex))
            return {
                "thresholdOn": 0,
                "thresholdOff": 0,
                "interval": 0,
            }

    def set_button_settings(self, option):
        """
        Function to update and save button settings in config file

        :param dict option: The button option to save
        :return: True if the settings were saved, False otherwise
        :rtype: bool
        """
        try:
            self.config.button_settings = option["option"]
            self.config.save_config(self.config.config)
            return True
        except Exception as ex:
            print('Error saving button settings: ' + str(ex))
            return False

    def get_button_settings(self):
        """
        Function to get button settings from config file

        :returns: Dictionary containing button settings
        :rtype: dict
        """
        try:
            return {"option": self.config.button_settings}
        except Exception as ex:
            print("Error getting button settings from config: " + str(ex))
            return {"option": 0}

    def get_version(self):
        """
        Function to get version number and date from config file

        :returns: Dictionary containing version number and date
        :rtype: dict
        """
        try:
            return {
                'number': self.config.version.get("version", "number"),
                'date': self.config.version.get("version", "date"),
            }
        except Exception as ex:
            print("Error getting version from config: " + str(ex))
            return {
                'number': '1.0',
                'date': ''
            }

    def get_update_version(self):
        """
        Function to get update version number and date from update path

        :returns: Dictionary containing version number and date
        :rtype: dict
        """
        try:
            config = self.config.update_version
            return {
                'number': config.get("version", "number"),
                'date': config.get("version", "date")
            }
        except Exception as ex:
            print("Error getting update version from config: " + str(ex))
            return {
                'number': '1.0',
                'date': ''
            }

    def check_updates(self):
        """
        Function to check for updates

        :returns: Dictionary containing update status
        :rtype: dict
        """

        response = {"update": False}
        try:
            current_version = Settings.get_version()

            os.system('mkdir ' + self.update_dir)
            os.system('wget --no-check-certificate --content-disposition https://github.com/BelardoA/picontrol/raw/master/picontrol.tgz')
            os.system('tar -xzf picontrol.tgz picontrol')
            os.system('mv ./picontrol ' + self.update_dir + '/picontrol')

            update_version = Settings.get_update_version()

            response = {"update": current_version['number'] != update_version['number']}

            os.system("sudo rm -R " + self.update_dir)
            os.system("sudo rm -R picontrol picontrol.tgz")
        except Exception as ex:
            print('Error when checking for updates: ' + str(ex))
            os.system("sudo rm -R " + self.update_dir)
            os.system("sudo rm -R picontrol picontrol.tgz")
            response = {"update": False}

        return response

    def update_version(self):
        """
        Function to check the version of the update and update the system

        :returns: Dictionary containing update status
        :rtype: dict
        """
        response = {"update": False}
        try:
            os.system('mkdir ' + self.update_dir)
            os.system('wget --no-check-certificate --content-disposition https://github.com/BelardoA/picontrol/raw/master/picontrol.tgz')
            os.system('tar -xzf picontrol.tgz picontrol')
            os.system('mv ./picontrol ' + self.update_dir + '/picontrol')
            os.system('cp ' + self.base_dir + '/configs/config.conf ' + self.update_dir + '/picontrol/configs/config.conf')
            print('copied config')
            os.system('sudo rm -R ' + self.base_dir)
            print('deleted base')
            os.system('cp -R ' + self.base_dir + '/picontrol ' + self.base_dir)
            print('copied update')

            os.system("sudo rm -R " + self.update_dir)
            os.system("sudo rm -R picontrol picontrol.tgz")
            response = {"update": Settings.get_version()["number"]}
        except Exception as ex:
            print('Error updating version: ' + str(ex))
            os.system("sudo rm -R " + self.update_dir)
            os.system("sudo rm -R picontrol picontrol.tgz")
            response = {"update": False}

        return response
