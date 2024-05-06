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


# Config file manager
class ConfigManager:
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
            'run_on_song_change': ''
        }

    # Create config folder
    def create_config_folder(self):
        if not os.path.exists(self.config_folder):
            os.makedirs(self.config_folder)

    # Create config file
    def create_config_file(self):
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as f:
                yaml.dump(self.default_config, f)

    # Create both config file and folder
    def create_config(self):
        if not os.path.exists(self.config_folder) or not os.path.exists(self.config_file):
            self.create_config_folder()
            self.create_config_file()

    # Return whether the file and folder exist or not
    def check_config(self):
        return os.path.exists(self.config_folder) and os.path.exists(self.config_file)

    # Load the config file
    def load_config(self):
        with open(self.config_file, 'r') as f:
            config_data = yaml.safe_load(f)
        return config_data

    # Extract value from config file using its key
    def get_value(self, key):
        config_data = self.load_config()
        # Returns a list if key is song_format
        # This ensures the value isn't returned empty or overwritten with the default
        # if the user changes it [value].
        # I love lasagna
        if key == 'song_format':
            return config_data.get(key, self.default_config[key]) or self.default_config[key]
        else:
            return config_data.get(key, self.default_config.get(key))
