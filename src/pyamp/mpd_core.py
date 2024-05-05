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
from mpd import MPDClient
from pyamp.config import ConfigManager


class MPDManager:
    def __init__(self):

        self.config_manager = ConfigManager()
        self.config_data = self.config_manager.load_config()
        self.host = self.config_data.get('host')
        self.port = self.config_data.get('port')

        self.client = MPDClient()
        try:
            self.client.connect(self.host, self.port)
        except Exception as e:
            print(f"Error connecting to MPD: {e}")
            exit()

    def get_client(self):
        return self.client
