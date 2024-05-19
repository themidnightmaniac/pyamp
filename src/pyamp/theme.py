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
    MAIN_OPTIONS_BACKGROUND,
    MAIN_NEXT,
    MAIN_PREV,
    MAIN_TOGGLE,
    MAIN_ALBUM,
    MAIN_STOP,
    MAIN_ADD
)
from resources.themes.mpipe.images import(
    MPIPE_BACKGROUND,
    MPIPE_SONG_PICKER_BACKGROUND,
    MPIPE_OPTIONS_BACKGROUND,
    MPIPE_NEXT,
    MPIPE_PREV,
    MPIPE_TOGGLE,
    MPIPE_ALBUM,
    MPIPE_STOP,
    MPIPE_ADD
)
from resources.themes.metal.images import(
    METAL_BACKGROUND,
    METAL_SONG_PICKER_BACKGROUND,
    METAL_OPTIONS_BACKGROUND,
    METAL_NEXT,
    METAL_PREV,
    METAL_TOGGLE,
    METAL_ALBUM,
    METAL_STOP,
    METAL_ADD
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
            spicker_stylesheet = self.read_css_file('../resources/themes/main/song_picker.css')
            options_stylesheet = self.read_css_file('../resources/themes/main/options.css')
            sp_background = MAIN_SONG_PICKER_BACKGROUND
            background = MAIN_BACKGROUND
            op_background = MAIN_OPTIONS_BACKGROUND
            next_img = MAIN_NEXT
            prev_img = MAIN_PREV
            toggle_img =MAIN_TOGGLE
            album_img = MAIN_ALBUM
            stop_img = MAIN_STOP
            add_img = MAIN_ADD
        elif self.theme == "midnight_pipe":
            stylesheet = self.read_css_file('../resources/themes/mpipe/styles.css')
            tbar_stylesheet = self.read_css_file('../resources/themes/mpipe/title_bar.css')
            spicker_stylesheet = self.read_css_file('../resources/themes/mpipe/song_picker.css')
            options_stylesheet = self.read_css_file('../resources/themes/mpipe/options.css')
            sp_background = MPIPE_SONG_PICKER_BACKGROUND
            op_background = MPIPE_OPTIONS_BACKGROUND
            background = MPIPE_BACKGROUND
            next_img = MPIPE_NEXT
            prev_img = MPIPE_PREV
            toggle_img = MPIPE_TOGGLE
            album_img = MPIPE_ALBUM
            stop_img = MPIPE_STOP
            add_img = MPIPE_ADD
        elif self.theme == "metal":
            stylesheet = self.read_css_file('../resources/themes/metal/styles.css')
            tbar_stylesheet = self.read_css_file('../resources/themes/metal/title_bar.css')
            spicker_stylesheet = self.read_css_file('../resources/themes/metal/song_picker.css')
            options_stylesheet = self.read_css_file('../resources/themes/metal/options.css')
            sp_background = METAL_SONG_PICKER_BACKGROUND
            op_background = METAL_OPTIONS_BACKGROUND
            background = METAL_BACKGROUND
            next_img = METAL_NEXT
            prev_img = METAL_PREV
            toggle_img = METAL_TOGGLE
            album_img = METAL_ALBUM
            stop_img = METAL_STOP
            add_img = METAL_ADD
        else:
            stylesheet = self.read_css_file('../resources/themes/main/styles.css')
            tbar_stylesheet = self.read_css_file('../resources/themes/main/title_bar.css')
            spicker_stylesheet = self.read_css_file('../resources/themes/main/song_picker.css')
            options_stylesheet = self.read_css_file('../resources/themes/main/options.css')
            sp_background = MAIN_SONG_PICKER_BACKGROUND
            op_background = MAIN_OPTIONS_BACKGROUND
            background = MAIN_BACKGROUND
            next_img = MAIN_NEXT
            prev_img = MAIN_PREV
            toggle_img =MAIN_TOGGLE
            album_img = MAIN_ALBUM
            stop_img = MAIN_STOP
            add_img = MAIN_ADD
        print(f"Using the {self.theme} theme.")
        return(
            sp_background,
            background,
            op_background,
            next_img,
            prev_img,
            toggle_img,
            album_img,
            stop_img,
            add_img,
            stylesheet,
            spicker_stylesheet,
            tbar_stylesheet,
            options_stylesheet,
            )
