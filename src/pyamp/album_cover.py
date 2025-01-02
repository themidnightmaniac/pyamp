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
import io
import os
from mutagen import File
from PIL import Image, ImageQt
from PySide6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class AlbumCoverWindow(QMainWindow):
    '''Window containing the current song's cover'''

    def __init__(self, mpd_manager, main_window):
        super().__init__()

        # Set up the window
        self.setWindowTitle("Pyamp - Album Art")
        self.setFixedSize(300, 300)  # Set window size to 300x300

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove any margins

        # Get the MPD client
        self.client = mpd_manager.get_client()

        # Connect the songChanged signal to the update_album_art slot
        main_window.songChanged.connect(self.update_album_art)

    def join_path(self):
        '''Return the current song's full path'''
        song_uri = self.client.currentsong().get("file")
        music_dir = os.environ.get("MUSIC_DIR")

        if song_uri and music_dir:
            absolute_song_path = os.path.join(music_dir, song_uri)

            # Check if the path contains '.cue'; If yes, strip the cue part to get the base directory
            # MPD Bug (or feature) that causes some songs uri to be what's in the cue sheet. ):
            if '.cue' in absolute_song_path.lower():
                # Strip the file name (which is the cue file) and get the parent directory
                song_dir = os.path.dirname(absolute_song_path)
                base_dir = os.path.dirname(song_dir)  # Get the parent directory of the cue file
                return base_dir + '/'  # Ensure trailing slash is appended (:
            return absolute_song_path
        return None

    def album_art_from_mpd(self, current_song):
        '''Return the art for the current song using mpd as a QPixmap'''
        try:
            album_art_data = self.client.albumart(current_song.get("file"))

            # Check if album art is returned in binary format or dict with binary key
            if isinstance(album_art_data, (bytes, dict)) and (
                isinstance(album_art_data, dict) and 'binary' in album_art_data or isinstance(album_art_data, bytes)
            ):
                binary_data = album_art_data['binary'] if isinstance(album_art_data, dict) else album_art_data
                pil_image = Image.open(io.BytesIO(binary_data))
                return QPixmap.fromImage(ImageQt.ImageQt(pil_image))
        except Exception:
            pass
        return None

    def album_art_from_metadata(self, file):
        '''Return the art for the current song using metadata as a QPixmap'''
        if file and os.path.isfile(file):
            try:
                audio = File(file)
                if 'covr' in audio.tags:
                    image_data = audio.tags['covr'][0]
                    pil_image = Image.open(io.BytesIO(image_data))
                    return QPixmap.fromImage(ImageQt.ImageQt(pil_image))
            except Exception:
                pass
        return None

    def album_art_from_directory(self, directory):
        '''Searches for image files in the specified directory'''
        if directory:
            image_extensions = ('.jpg', '.jpeg', '.png', '.gif')
            for filename in os.listdir(directory):
                if filename.lower().endswith(image_extensions):
                    return os.path.join(directory, filename)
        return None

    def update_album_art(self):
        '''Get the album art for the current song and call show_album_art on it'''
        # Clear the layout before adding new album art
        self.clear_layout(self.layout)

        # Get current song info
        current_song = self.client.currentsong()
        # Try setting album art using MPD's native art feature
        album_art = self.album_art_from_mpd(current_song)

        # If MPD album art retrieval fails, fall back to file metadata
        if not album_art:
            absolute_song_path = self.join_path()
            album_art = self.album_art_from_metadata(absolute_song_path) if absolute_song_path else None

        # If both MPD and metadata fail, try finding an image in the song's directory
        if not album_art:
            song_dir = os.path.dirname(absolute_song_path) if absolute_song_path else None
            if song_dir:
                image_path = self.album_art_from_directory(song_dir)
                if image_path:
                    pil_image = Image.open(image_path)
                    album_art = QPixmap.fromImage(ImageQt.ImageQt(pil_image))

        # If no album art was found (skill issue)
        if not album_art:
            self.show_no_album_art_found()
        else:
            self.show_album_art(album_art)

    def clear_layout(self, layout):
        '''Clear all widgets from the given layout'''
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    def show_no_album_art_found(self):
        '''Display "No album art found." message in the parent widget'''
        label = QLabel("No album art found.")
        label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label)

    def show_album_art(self, album_art):
        '''Set the background of the parent layout as the given image (QPixmap)'''
        label = QLabel()
        label.setPixmap(album_art.scaledToWidth(300, mode=Qt.SmoothTransformation))
        label.setScaledContents(True)
        self.layout.addWidget(label)

    def keyPressEvent(self, event):  # pylint: disable=C0103
        '''Close the window on q or esc key press'''
        if event.key() in (Qt.Key_Q, Qt.Key_Escape):
            self.close()
