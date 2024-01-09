# read version from configs/picontrol.version

from configparser import ConfigParser


def load_version():
    """
    Load the version file from disk (picontrol.version)
    """
    version = ConfigParser()
    version.read('/home/pi/scripts/picontrol/configs/picontrol.version')
    version = version.get('version', 'number')
    return version


__version__ = load_version()
