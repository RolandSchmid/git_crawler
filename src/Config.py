import configparser
import os
from datetime import datetime

# Timestamp
main_timestamp = datetime.now().strftime("%Y-%m-%d %H%M%S")

# File paths
dir_root = '../'
default_data = dir_root + 'data/'
default_out = dir_root + 'out/'
default_repos = default_out + 'repos/'
ini_name = 'config.ini'

# Thread settings
default_n_git_threads = 4
default_n_file_threads = 1

config = configparser.ConfigParser()
config.read(dir_root + ini_name)


class Config:

    @classmethod
    def get_timestamp(cls):
        return main_timestamp

    @classmethod
    def get_dir_data(cls):
        return cls.get_config_param('file_path', 'dir_data', default_data)

    @classmethod
    def get_dir_out(cls):
        return cls.get_config_param('file_path', 'dir_out', default_out)

    @classmethod
    def get_dir_repos(cls):
        return cls.get_config_param('file_path', 'dir_repos', default_repos)

    @classmethod
    def get_n_git_threads(cls):
        return cls.get_config_int('threads', 'n_git_threads', str(default_n_git_threads))

    @classmethod
    def get_n_file_threads(cls):
        return cls.get_config_int('threads', 'n_file_threads', str(default_n_file_threads))

    @classmethod
    def is_clean_repo(cls):
        return cls.get_config_bool('cleanup', 'clean_repos', True)

    @classmethod
    def get_config_param(cls, section, option, default):
        cls.create_if_not_exists(section, option, default)
        return config[section].get(option, default)

    @classmethod
    def get_config_int(cls, section, option, default):
        cls.create_if_not_exists(section, option, default)
        return config[section].getint(option, default)

    @classmethod
    def get_config_bool(cls, section, option, default):
        cls.create_if_not_exists(section, option, default)
        return config[section].getboolean(option, default)

    @classmethod
    def create_if_not_exists(cls, section, option, default):
        if not config.has_section(section) or not config.has_option(section, option):
            if not config.has_section(section):
                config[section] = {option: default}
            if not config.has_option(section, option):
                config[section][option] = default
        with open(dir_root + ini_name, 'w') as configfile:
            config.write(configfile)


# Init values
Config.get_dir_data()
Config.get_dir_out()
Config.get_dir_repos()
Config.get_n_git_threads()
Config.get_n_file_threads()
Config.is_clean_repo()

# Create repos folder
if not os.path.exists(Config.get_dir_repos()):
    os.makedirs(Config.get_dir_repos())
