#!/usr/bin/python 
#config.py

import ConfigParser


class Config:
    config_file = 'config.conf'
    base_path = '/home/pi/scripts/picontrol/configs'
    update_path = '/home/pi/scripts/picontrol_update/picontrol/configs'

    def loadConfig(self):
        config = ConfigParser.RawConfigParser()
        configFilePath = self.base_path + self.config_file
        config.read(configFilePath)
        return config
    
    def saveConfig(self, config):
        with open(self.base_path + self.config_file, 'w') as configFile:
            config.write(configFile)
        return True

    def loadVersion(self):
        config = ConfigParser.RawConfigParser()
        configFilePath = self.base_path + '/picontrol.version'
        config.read(configFilePath)
        return config
    
    def saveVersion(self, config):
        with open(self.base_path + '/picontrol.version', 'w') as configFile:
            config.write(configFile)
        return True

    def loadUpdateVersion(self):
        config = ConfigParser.RawConfigParser()
        configFilePath = self.update_path + '/picontrol.version'
        config.read(configFilePath)
        return config
