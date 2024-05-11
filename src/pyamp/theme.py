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
from pyamp.config import ConfigManager
from resources.themes.main.images import(
    MAIN_BACKGROUND,
    MAIN_SONG_PICKER_BACKGROUND,
    MAIN_NEXT,
    MAIN_PREV,
    MAIN_TOGGLE,
    MAIN_ALBUM,
    MAIN_STOP,
    MAIN_ADD
)
from resources.themes.midnight_pipe.images import(
    MPIPE_BACKGROUND,
    MPIPE_SONG_PICKER_BACKGROUND,
    MPIPE_NEXT,
    MPIPE_PREV,
    MPIPE_TOGGLE,
    MPIPE_ALBUM,
    MPIPE_STOP,
    MPIPE_ADD
)

class ThemeManager():
    '''Manages the program themes'''
    def __init__(self):
        config_manager = ConfigManager()
        self.theme = config_manager.get_value("theme")

    def read_css_file(self, relative_path):
        '''Placeholder'''
        # Get the directory of the current script
        current_dir = os.path.dirname(__file__)

        # Construct the absolute path using the current directory and the relative path
        absolute_path = os.path.abspath(os.path.join(current_dir, relative_path))

        # Read the contents of the CSS file
        with open(absolute_path, 'r', encoding='UTF-8') as css_file:
            css_content = css_file.read()

        return css_content

    def get_theme(self):
        '''Returns the stylesheet and images for each theme'''
        if self.theme == "main":
            stylesheet = self.read_css_file('../resources/themes/main/styles.css')
            tbar_stylesheet = self.read_css_file('../resources/themes/main/title_bar.css')
            return(
                MAIN_SONG_PICKER_BACKGROUND,
                MAIN_BACKGROUND,
                MAIN_NEXT,
                MAIN_PREV,
                MAIN_TOGGLE,
                MAIN_ALBUM,
                MAIN_STOP,
                MAIN_ADD,
                stylesheet,
                tbar_stylesheet
            )
        elif self.theme == "midnight_pipe":
            stylesheet = self.read_css_file('../resources/themes/midnight_pipe/styles.css')
            tbar_stylesheet = self.read_css_file('../resources/themes/midnight_pipe/title_bar.css')
            return(
                MPIPE_SONG_PICKER_BACKGROUND,
                MPIPE_BACKGROUND,
                MPIPE_NEXT,
                MPIPE_PREV,
                MPIPE_TOGGLE,
                MPIPE_ALBUM,
                MPIPE_STOP,
                MPIPE_ADD,
                stylesheet,
                tbar_stylesheet
            )
        else:
            stylesheet = self.read_css_file('../resources/themes/main/styles.css')
            return(
                MAIN_SONG_PICKER_BACKGROUND,
                MAIN_BACKGROUND,
                MAIN_NEXT,
                MAIN_PREV,
                MAIN_TOGGLE,
                MAIN_ALBUM,
                MAIN_STOP,
                MAIN_ADD,
                stylesheet
            )
