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
from PySide6.QtWidgets import QApplication
import sys

from pyamp.main_window import MainWindow
from pyamp.mpd_core import MPDManager
from pyamp.config import ConfigManager


def main():
    print("Pyamp  Copyright (C) 2024  Ignacio Gonsalves\nThis program comes with ABSOLUTELY NO WARRANTY;\nThis is free software, and you are welcome to redistribute it under certain conditions.")
    config_manager = ConfigManager()
    if not config_manager.check_config():
        config_manager.create_config()
        print("Successfully wrote config file/folder!")
    else:
        print("Config folder and file are present.")
    app = QApplication(sys.argv)
    mpd_manager = MPDManager()
    window = MainWindow(mpd_manager)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
