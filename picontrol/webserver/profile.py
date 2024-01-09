#!/usr/bin/python 
# profile.py

from config import Config


class Profile:
    def __init__(self):
        self.config = Config()

    def set_user(self, user):
        """
        Update and save user in config file

        :param dict user: The user to save in config file
        :return: True if the user was saved, False otherwise
        :rtype: bool
        """
        try:
            config = self.config
            config.user['username'] = user['username']
            config.user["password"] = user['password']
            config.save_config(config.config)
            return True
        except Exception as ex:
            print('Error saving user: ' + str(ex))
            return False

    def get_user(self) -> dict:
        """
        Function to get user info from config file

        :returns: Dictionary containing username and password
        :rtype: dict
        """
        try:
            return self.config.user
        except Exception as ex:
            print('Error getting user: ' + str(ex))
            return {"username": '', "password": ''}

    @staticmethod
    def set_theme(theme):
        try:
            config = Config().config
            config.theme = theme["theme"]
            
            config.save_config(config)
            return True
        except Exception as ex:
            print('Error saving theme: ' + str(ex))
            return False

    @staticmethod
    def get_theme():
        try:
            return {"theme": Config().theme}
        except Exception as ex:
            print('Error getting theme: ' + str(ex) + '. Using default theme.')
            return {"theme": 'green'}

            