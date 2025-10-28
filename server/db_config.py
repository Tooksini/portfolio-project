import configparser
import os

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db_config.properties')
config.read(config_path)

DB_CONFIG = {
    'host': config.get('DEFAULT', 'host'),
    'user': config.get('DEFAULT', 'user'),
    'password': config.get('DEFAULT', 'password'),
    'database': config.get('DEFAULT', 'database'),
    'port': config.getint('DEFAULT', 'port')
}

