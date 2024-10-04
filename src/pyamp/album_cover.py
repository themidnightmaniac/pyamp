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
import io
import os
from mutagen import File
from PIL import Image, ImageQt
from PySide6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class AlbumCoverWindow(QMainWindow):
    '''Creates a window, displaying the current song's album cover art'''
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

    def join_path(self):
        '''Joins the $MUSIC_DIR environment variable with the current song's uri'''
        current_song_info = self.client.currentsong()
        song_uri = current_song_info.get("file")
        music_dir = os.environ.get("MUSIC_DIR")

        if song_uri and music_dir:
            absolute_song_path = os.path.join(music_dir, song_uri)

            # Check if the path contains '.cue'; This is a mpd bug (or feature) that causes the path to be what's in the cue sheet.
            if '.cue' in absolute_song_path.lower():
                print(absolute_song_path)
                return None

            return absolute_song_path
        return None

    def extract_album_art(self, file):
        '''Extracts the album art from the current song's file metadata'''
        if file:
            try:
                # Ensure the file exists and is a file
                if not os.path.isfile(file):
                    print(f"File not found or not a file: {file}")
                    return None

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
                else:
                    image = None

                return image
            except Exception as e:
                print(f"Album art error: {e}. MPD probably isn't playing.")
        return None

    def update_album_art(self):
        '''Displays the album art'''

        # Construct the absolute path of the song
        absolute_song_path = self.join_path()
        if absolute_song_path:
            song_dir = os.path.dirname(absolute_song_path)
        else:
            song_dir = None

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
            if song_dir:  # Ensure song_dir is valid
                image_path = self.find_image_in_directory(song_dir)

                if image_path:
                    pil_image = Image.open(image_path)
                    qpixmap = QPixmap.fromImage(ImageQt.ImageQt(pil_image))
                    label = QLabel()
                    label.setPixmap(qpixmap.scaledToWidth(300, mode=Qt.SmoothTransformation))
                    label.setScaledContents(True)
                    layout.addWidget(label)
                else:
                    label = QLabel("No album art found.")
                    label.setAlignment(Qt.AlignCenter)
                    layout.addWidget(label)
            else:
                label = QLabel("No album art found.")
                label.setAlignment(Qt.AlignCenter)
                layout.addWidget(label)

    def find_image_in_directory(self, directory):
        '''Searches for image files in the specified directory'''
        if directory:
            image_extensions = ('.jpg', '.jpeg', '.png', '.gif')
            for filename in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, filename)) and filename.lower().endswith(image_extensions):
                    return os.path.join(directory, filename)
        return None


    def keyPressEvent(self, event): # pylint: disable=C0103
        '''Closes the window on q or escape key press'''
        if event.key() == Qt.Key_Q or event.key() == Qt.Key_Escape:
            self.close()
