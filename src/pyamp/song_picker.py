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
import base64
from PySide6.QtWidgets import (
    QMainWindow,
    QLineEdit,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QListWidgetItem,
    QListWidget,
    QAbstractItemView
)
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt, Signal
from pyamp.ui import createTitleBar

class SongItem(QListWidgetItem):
    '''Song item'''
    def __init__(self, title, uri):
        super().__init__(title)
        self.uri = uri


class SongPickerWindow(QMainWindow):
    '''Window to select and add songs to the queue'''
    window_close = Signal()

    def __init__(self, mpd_manager, img_song_picker_background, spicker_stylesheet, tbar_stylesheet):
        super().__init__()
        # Window title and geometry
        self.setWindowTitle("Pyamp - Song Picker")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(0, 0, 410, 770)
        self.setFixedSize(self.size())

        img_background = img_song_picker_background
        stylesheet = spicker_stylesheet

        # Window background and alpha channel
        # Decode the base64 image data
        background_data = base64.b64decode(img_background)

        # Create a QPixmap from the binary data
        background_pixmap = QPixmap()
        background_pixmap.loadFromData(background_data)

        # Set the background image and mask
        self.background_image = background_pixmap
        self.setMask(self.background_image.mask())

        # Layout and central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # MPD client
        self.client = mpd_manager.get_client()

        # Title bar
        self.title_bar = createTitleBar(self, "Pyamp 1.0 - Song Picker", tbar_stylesheet, mpd_manager, None, None, button=False)
        self.setMenuWidget(self.title_bar)

        # Containers

        # Buttons container
        self.button_container = QWidget()
        self.button_container_layout = QHBoxLayout(self.button_container)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.filter_options)
        self.search_bar.setStyleSheet(stylesheet)
        self.layout.addWidget(self.search_bar)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(stylesheet)
        self.list_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.list_widget.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.layout.addWidget(self.list_widget)

        # Buttons
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.on_ok_clicked)
        self.ok_button.setStyleSheet(stylesheet)
        self.button_container_layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close_song_picker)
        self.cancel_button.setStyleSheet(stylesheet)
        self.button_container_layout.addWidget(self.cancel_button)

        self.clear_button = QPushButton("Clear Queue")
        self.clear_button.setStyleSheet(stylesheet)
        self.button_container_layout.addWidget(self.clear_button)
        self.clear_button.clicked.connect(self.clear_queue)

        self.layout.addWidget(self.button_container)

        self.delay_active = None

        self.fetch_songs()

    def clear_queue(self):
        '''Clear the MPD queue'''
        self.client.clear()

    def paintEvent(self, event): # pylint: disable=invalid-name,unused-argument
        '''Draw the window with a background image'''
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_image)
        self.delay_active = False

    def fetch_songs(self):
        '''Fetch songs from MPD'''
        # Clear the widget
        self.list_widget.clear()
        # Get all songs
        songs = self.client.listallinfo()
        # Gotta Display 'em all
        for song in songs:
            title = song.get("title", None)
            if title:
                item = SongItem(title, song.get("file", ""))
                self.list_widget.addItem(item)

    def filter_options(self):
        '''Filter displayed songs by search'''
        search_text = self.search_bar.text().lower()
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            # Hide all items that dont match the search string
            if search_text in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def add_selected_songs(self):
        '''Add selected songs to the queue'''
        selected_indexes = [index.row() for index in self.list_widget.selectedIndexes()]
        selected_songs = []
        for index in selected_indexes:
            item = self.list_widget.item(index)
            selected_songs.append(item.uri)
        for song in selected_songs:
            self.client.add(song)

    def clear_selection(self):
        '''Clear the song selection'''
        self.list_widget.clearSelection()

    def on_ok_clicked(self):
        '''Close the window and updates song display when OK is pressed'''
        self.window_close.emit()
        self.add_selected_songs()
        self.close()

    def close_song_picker(self):
        '''Close the song picker window'''
        self.close()
        self.window_close.emit()
