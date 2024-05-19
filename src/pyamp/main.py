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
import sys
from PySide6.QtWidgets import QApplication
from pyamp.main_window import MainWindow
from pyamp.mpd_core import MPDManager
from pyamp.config import ConfigManager


def main():
    '''Runs Pyamp'''
    print(
    "Pyamp 0.1.1 - Copyright (C) 2024  Ignacio Gonsalves"
    )
    config_manager = ConfigManager()
    if not config_manager.check_config():
        try:
            config_manager.create_config()
            print("Successfully created config file/folder!")
        except Exception as e:
            print("An error ocurred while creating the config file/folder: ", e)
    app = QApplication(sys.argv)
    mpd_manager = MPDManager()
    window = MainWindow(mpd_manager)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
