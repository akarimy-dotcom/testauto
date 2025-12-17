"""
Import classes from libs folder.
Report class it is used to create an object to use both in EM and TDM operations
"""
from libs.ConfigParser import ConfigParser

# Initialize the configuration parser
configs = ConfigParser("./configs/Config.txt")
# store configuration in variables

device_config = configs.get_configuration("device_config")
