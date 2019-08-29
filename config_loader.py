# config_loader.py
from configparser import SafeConfigParser
import os

class Config:
    """Interact with configuration variables."""

    configParser = SafeConfigParser()
    configFilePath = (os.path.join(os.getcwd(), 'config.ini'))
    configParser.read('config.ini')

    @classmethod
    def initialize(cls, key):
        """Start config by reading config.ini."""
        cls.configParser.read(cls.configFilePath)

    @classmethod
    def paths(cls, key):
        """Get path values from config.ini."""
        return cls.configParser.get('PATHS', key)

    @classmethod
    def dev(cls, key):
        """Get dev values from config.ini."""
        return cls.configParser.get('DEV', key)