#    Pyamp - Minimal MPD client written in Python using Qt
#    Copyright (C) 2024  Ignacio Gonsalves
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os
import yaml


class ConfigManager:
    '''Manages the program configuration and configuration file'''
    def __init__(self, config_file="config.yaml"):
        # Set the config file
        self.config_file = os.path.expanduser("~/.config/pyamp/" + config_file)
        # Set the config path
        self.config_folder = os.path.dirname(self.config_file)
        # Set the default config
        self.default_config = {
            'host': 'localhost',
            'port': '6600',
            'song_format': ['title', 'artist', 'album'],
            'run_on_song_change': '',
            'theme': 'main',
        }

    def create_config_folder(self):
        '''Creates the config folder'''
        if not os.path.exists(self.config_folder):
            os.makedirs(self.config_folder)

    def create_config_file(self):
        '''Creates the config file'''
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w', encoding="utf-8") as f:
                yaml.dump(self.default_config, f)

    def create_config(self):
        '''If theres no config file or folder, create both'''
        if not os.path.exists(self.config_folder) or not os.path.exists(self.config_file):
            self.create_config_folder()
            self.create_config_file()

    def check_config(self):
        '''Checks if config file and folder exist'''
        return os.path.exists(self.config_folder) and os.path.exists(self.config_file)

    def load_config(self):
        '''Loads the config file'''
        with open(self.config_file, 'r', encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
        return config_data

    def get_value(self, key):
        '''Gets the value from the config file key/item'''
        config_data = self.load_config()
        # Returns a list if key is song_format
        # This ensures the value isn't returned empty or overwritten with the default
        # if the user changes it [value].
        # I love lasagna
        if key == 'song_format':
            data = config_data.get(key, self.default_config[key]) or self.default_config[key]
        else:
            data = config_data.get(key, self.default_config.get(key))
        return data
