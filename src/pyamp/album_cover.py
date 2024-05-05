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
from mutagen import File
from PIL import Image, ImageQt
import io
import os
from PySide6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


# Album cover display window
class AlbumCoverWindow(QMainWindow):
    def __init__(self, mpd_manager, main_window):
        super().__init__()

        # Set up the window
        self.setWindowTitle("Pyamp - Album Art")
        self.setFixedSize(300, 300)  # Set window size to 300x300

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove any margins

        # Get the mpd client
        self.client = mpd_manager.get_client()

        # Connect the songChanged signal to the update_album_art slot
        main_window.songChanged.connect(self.update_album_art)

    # This func joins the $MUSIC_DIR path with the current song uri
    def join_path(self):
        # Gets the current song uri from mpd
        current_song_info = self.client.currentsong()
        song_uri = current_song_info.get("file")
        # Gets the $MUSIC_DIR env variable
        music_dir = os.environ.get("MUSIC_DIR")
        if not song_uri or not music_dir:
            return
        else:
            absolute_song_path = os.path.join(music_dir, song_uri)
            return absolute_song_path

    # This func extracts the album art from the audio file
    def extract_album_art(self, file):
        try:
            # Open the audio file
            audio = File(file)
            # Extract the album art if available
            if audio and 'covr' in audio.tags:
                # Get the first album art (there might be multiple)
                image_data = audio.tags['covr'][0]
                # Convert image data to PIL Image
                pil_image = Image.open(io.BytesIO(image_data))
                # Convert PIL Image to QPixmap
                image = QPixmap.fromImage(ImageQt.ImageQt(pil_image))
                print("Album art found.")
                return image
            else:
                print("No album art found.")
                return None
        except Exception as e:
            print(f"Error: {e}. MPD probably isn't playing.")
            return None

    # This func displays the album art
    def update_album_art(self):
        # Get the absolute path of the currently playing song
        absolute_song_path = self.join_path()

        # Extract the album art for the current song
        album_art = self.extract_album_art(absolute_song_path)

        # Clear the layout before adding the new album art
        layout = self.centralWidget().layout()
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

        # Add the album art to the layout
        if album_art:
            label = QLabel()
            label.setPixmap(album_art.scaledToWidth(300, mode=Qt.SmoothTransformation))
            label.setScaledContents(True)
            layout.addWidget(label)
        else:
            print("No album art found.")
            label = QLabel("No album art found.")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)

    # Close the window on q or escape press
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q or event.key() == Qt.Key_Escape:
            self.close()
