#    Pyamp - Minimal MPD client written in Python using Qt
#    Copyright (C) 2025  Ignacio Gonsalves
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
import sys
from mpd import MPDClient
from pyamp.config import ConfigManager


class MPDManager:
    '''Creates the MPD client'''
    def __init__(self):

        # Load config
        self.config_manager = ConfigManager()
        self.config_data = self.config_manager.load_config()
        # Set host and port from config
        self.host = self.config_data.get('host')
        self.port = self.config_data.get('port')

        # Open client
        self.client = MPDClient()
        try:
            self.client.connect(self.host, self.port)
        except Exception as e:
            print(f"Error connecting to MPD: {e}")
            sys.exit()

    def get_client(self):
        '''Return the MPD client'''
        return self.client
