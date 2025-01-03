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
import subprocess
from time import strftime, localtime
import base64
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QProgressBar,
    QGridLayout,
    QSlider,
    QSizePolicy,
    QHBoxLayout,
    QLabel,
    QVBoxLayout
)
from PySide6.QtGui import QPixmap, QPainter, QFont, QIcon, QImage
from PySide6.QtCore import QTimer, Qt, Signal
from pyamp.song_picker import SongPickerWindow
from pyamp.album_cover import AlbumCoverWindow
from pyamp.ui import createTitleBar, NonSelectableLineEdit, CreateSpacer
from pyamp.config import ConfigManager
from pyamp.theme import ThemeManager


# Main window
class MainWindow(QMainWindow):
    '''Main window'''
    # Define the song changed signal for the album cover display
    songChanged = Signal()

    def __init__(self, mpd_manager):
        super().__init__()

        # Window title and geometry
        self.setWindowTitle("Pyamp")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 400, 160)
        self.setFixedSize(self.size())

        theme_manager = ThemeManager()

        (
            img_song_picker_background,
            img_background,
            img_op_background,
            img_next,
            img_prev,
            img_toggle,
            img_album,
            img_stop,
            img_add,
            stylesheet,
            spicker_stylesheet,
            tbar_stylesheet,
            options_stylesheet,
        ) = theme_manager.get_theme()

        # Window background and alpha channel
        # Decode the base64 image data
        background_data = base64.b64decode(img_background)

        # Create a QPixmap from the binary data
        background_pixmap = QPixmap()
        background_pixmap.loadFromData(background_data)

        # Set the background image and mask
        self.background_image = background_pixmap
        self.setMask(self.background_image.mask())

        # Config file
        self.config_manager = ConfigManager()
        self.song_order = self.config_manager.get_value("song_format")
        self.user_command = self.config_manager.get_value("run_on_song_change")

        # MPD setup
        self.client = mpd_manager.get_client()
        self.mpd_status = self.client.status()
        self.playstate = ""
        self.songs_played = 0
        self.current_song = ''
        self.current_song_title = ''
        self.current_artist = ''
        self.current_album = ''
        if not self.song_order:
            self.song_format = "{playstate} {title} - {artist} - {album}"
            print("Song format is empty, falling back to the default format")
        else:
            try:
                self.song_format = "{playstate} " + " - ".join(
                    ["{" + item + "}" for item in self.song_order]
                    )
            except Exception as e:
                print(
                    f"An error occurred while reading the song format from the config file: "
                    f"{e}. Falling back to the default format"
                )

                self.song_format = "{playstate} {title} - {artist} - {album}"

        # Clock setup
        self.current_time = strftime("%H:%M")

        # Central widget config
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        font = QFont("Terminus")
        QApplication.setFont(font)

        # Layout config
        self.layout = QGridLayout(central_widget)
        central_widget.setLayout(self.layout)
        self.layout.setContentsMargins(5, 5, 5, 5)

        # Spacers
        self.spacer1 = CreateSpacer(8, 8, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addItem(self.spacer1, 1, 1, 2, 1)
        self.spacer2 = CreateSpacer(8, 8, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addItem(self.spacer2, 1, 3, 2, 1)

        # Title bar
        self.title_bar = createTitleBar(self, "Pyamp 1.1.0", tbar_stylesheet, mpd_manager, img_op_background, options_stylesheet, button=True)
        self.setMenuWidget(self.title_bar)

        # Containers
        # Displays container
        self.display_container = QWidget()
        self.display_container_layout = QHBoxLayout(self.display_container)
        self.display_container_layout.setContentsMargins(0, 0, 2, 0)
        self.layout.addWidget(self.display_container, 1, 2, 1, 1)

        # Song name and elapsed bar container
        self.song_container = QWidget()
        self.song_container_layout = QVBoxLayout(self.song_container)
        self.song_container_layout.setContentsMargins(0, 0, 0, 2)
        self.display_container_layout.addWidget(self.song_container)

        # Panel container
        self.panel_container = QWidget()
        self.panel_container_layout = QVBoxLayout(self.panel_container)
        self.panel_container_layout.setContentsMargins(0, 0, 0, 2)
        self.layout.addWidget(self.panel_container, 2, 2, 1, 1)

        # Clock Display
        self.clock_display = QLabel()
        self.clock_display.setStyleSheet(stylesheet)
        self.clock_display.setText(self.current_time)
        self.clock_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.display_container_layout.addWidget(self.clock_display)
        self.display_container_layout.insertWidget(0, self.clock_display)

        # Timer for updating the clock display in realtime.
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.clock_update)

        # Song display
        self.song_display = NonSelectableLineEdit(central_widget)
        self.song_display.setStyleSheet(stylesheet)
        self.song_display.setFixedHeight(30)
        self.song_display.setFixedWidth(260)
        self.song_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.song_display.setReadOnly(True)
        self.song_display.setCursorPosition(0)
        self.song_container_layout.addWidget(self.song_display)
        self.song_container_layout.insertWidget(0, self.song_display)

        # Timer to scroll the current song text
        self.scroll_timer = QTimer(self)
        self.scroll_timer.timeout.connect(self.scroll_text)
        self.delay_active = None

        # Progress bar
        self.progress_bar = QProgressBar(central_widget)
        self.progress_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.progress_bar.setStyleSheet(stylesheet)
        self.progress_bar.setFixedHeight(20)
        self.song_container_layout.addWidget(self.progress_bar)

        # Timer to update progress bar periodically
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress)

        # Volume slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setFixedHeight(15)
        self.volume_slider.setStyleSheet(stylesheet)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        mpd_volume = self.get_slider_value()
        self.volume_slider.setValue(mpd_volume)
        self.volume_slider.valueChanged.connect(self.volume_changed)
        self.panel_container_layout.addWidget(self.volume_slider)
        self.panel_container_layout.insertWidget(0, self.volume_slider)

        # Buttons Container
        self.button_container = QWidget()
        self.button_container_layout = QHBoxLayout(self.button_container)
        self.button_container_layout.setContentsMargins(0, 5, 0, 0)
        self.panel_container_layout.addWidget(self.button_container)

        # Buttons
        # Previous song button
        prev_icon = QIcon(QPixmap.fromImage(QImage.fromData(base64.b64decode(img_prev))))
        self.prev = QPushButton("", self)
        self.prev.setFixedHeight(25)
        self.prev.setFixedWidth(25)
        self.button_container_layout.addWidget(self.prev)
        self.prev.setIcon(prev_icon)
        self.prev.setStyleSheet(stylesheet)
        self.prev.clicked.connect(self.on_prev_press)

        # Stop button
        stop_icon = QIcon(QPixmap.fromImage(QImage.fromData(base64.b64decode(img_stop))))
        self.stop = QPushButton("", self)
        self.stop.setFixedHeight(25)
        self.stop.setFixedWidth(25)
        self.button_container_layout.addWidget(self.stop)
        self.stop.setIcon(stop_icon)
        self.stop.setStyleSheet(stylesheet)
        self.stop.clicked.connect(self.on_stop_press)

        # Play/Pause button
        toggle_icon = QIcon(QPixmap.fromImage(QImage.fromData(base64.b64decode(img_toggle))))
        self.toggle = QPushButton("", self)
        self.toggle.setCheckable(True)
        self.toggle.setFixedHeight(25)
        self.toggle.setFixedWidth(25)
        self.button_container_layout.addWidget(self.toggle)
        self.toggle.setIcon(toggle_icon)
        self.toggle.setStyleSheet(stylesheet)
        self.toggle.clicked.connect(self.on_play_toggle)

        # Song picker button
        add_icon = QIcon(QPixmap.fromImage(QImage.fromData(base64.b64decode(img_add))))
        self.add = QPushButton("", self)
        self.add.setFixedHeight(25)
        self.add.setFixedWidth(25)
        self.button_container_layout.addWidget(self.add)
        self.add.setIcon(add_icon)
        self.add.setStyleSheet(stylesheet)
        self.song_picker_window = SongPickerWindow(
            mpd_manager,
            img_song_picker_background,
            spicker_stylesheet,
            tbar_stylesheet,
        )
        self.add.clicked.connect(self.open_song_picker)

        # Next song button
        next_icon = QIcon(QPixmap.fromImage(QImage.fromData(base64.b64decode(img_next))))
        self.next = QPushButton("", self)
        self.next.setFixedHeight(25)
        self.next.setFixedWidth(25)
        self.button_container_layout.addWidget(self.next)
        self.next.setIcon(next_icon)
        self.next.setStyleSheet(stylesheet)
        self.next.clicked.connect(self.on_next_press)

        # Album art button
        album_icon = QIcon(QPixmap.fromImage(QImage.fromData(base64.b64decode(img_album))))
        self.album = QPushButton("", self)
        self.album.setFixedHeight(25)
        self.album.setFixedWidth(25)
        self.button_container_layout.addWidget(self.album)
        self.album.setIcon(album_icon)
        self.album.setStyleSheet(stylesheet)
        self.album_display = AlbumCoverWindow(mpd_manager, self)
        self.album.clicked.connect(lambda: self.album_display.show()) # pylint: disable=W0108

        # Timer checking for song changes
        self.check_song_change_timer = QTimer(self)
        self.check_song_change_timer.timeout.connect(self.check_song_change)
        self.previous_song = None

        # duhh
        self.startup()

    def startup(self):
        '''Start timers, check playstate and song'''
        # Check mpd status
        if self.mpd_status.get("state") == "play":
            # Set status and button to "play"
            self.toggle.setChecked(True)
            self.playstate = "Playing:"
        elif self.mpd_status.get("state") == "pause":
            # Set status and button to "pause"
            self.toggle.setChecked(False)
            self.playstate = "Paused:"
        else:
            self.playstate = "Not Playing!"
        # Start timers
        self.song_changed()
        self.check_song_change_timer.start(1000)
        self.scroll_timer.start(80)
        self.progress_timer.start(1000)
        self.update_clock_timer()
        self.clock_timer.start()

    def check_song_change(self):
        '''Check if the current song changed'''
        try:
            # Check for song change
            current_song = self.client.currentsong()
            if current_song != self.previous_song:
                # Update the current song info
                self.previous_song = current_song
                self.songChanged.emit()

                # Try to run run_on_song_change command
                self.run_user_command("song_change")

                # Skip the first current song var update
                if self.songs_played == 0:
                    # If no song has played yet, increment the counter by 1
                    self.songs_played += 1
                else:
                    # Update the song display
                    self.song_changed()
                    # Increment the songs played counter on every song change
                    self.songs_played += 1

        except Exception as e:
            print("Connection error:", e)
            self.close()

    def run_user_command(self, cmd_arg):
        '''Run a command specified in the config file for every song changed, re passing the passed arg'''
        if self.user_command:
            command = self.user_command + f" {cmd_arg}"
            try:
                global subprocess_instance
                with subprocess.Popen(command.split()) as subprocess_instance:
                    subprocess_instance.communicate()
            except Exception as e:
                print("An error occurred while running the custom command: ", e)

    def get_current_song_info(self):
        '''Get all info from the current song'''
        try:
            status = self.client.status()
            if status.get("state") == "stop":
                # Set the current song variable
                self.current_song = "Not Playing!"
            else:
                # Fetch MPD's current song info
                current_song_info = self.client.currentsong()

                # Set the current song variable
                self.current_song_title = current_song_info.get("title")
                self.current_artist = current_song_info.get("artist")
                self.current_album = current_song_info.get("album")

                # Use current_song_format to construct current_song string
                self.current_song = self.song_format.format(
                    playstate=self.playstate,
                    title=self.current_song_title,
                    artist=self.current_artist,
                    album=self.current_album,
                )

            # Return the current song variable
            return self.current_song
        except Exception as e:
            print(f"An error occurred while getting current song info: {e}")
            return None

    def song_changed(self):
        '''Update the screen with the new song's info'''
        state = self.mpd_status.get("state")
        if state in ["play", "pause", "stop"]:
            self.current_song = self.get_current_song_info()
            self.song_display.setText(self.current_song)
            self.song_display.setCursorPosition(0)
        else:
            self.current_song = "Not Playing!"
            self.song_display.setText(self.current_song)
            self.song_display.setCursorPosition(0)

    def get_slider_value(self):
        '''Set the slider position to the volume reported by mpd'''
        try:
            if self.mpd_status.get("state") != "stop":
                slider_value = int(self.client.status()["volume"])
            else:
                slider_value = 50
        except Exception:
            slider_value = 50
        return slider_value

    def volume_changed(self, value):
        '''Change the mpd volume on slider update'''
        try:
            self.client.setvol(value)
        except Exception as e:
            print(f"An error occurred while setting the volume: {e}")

    def update_progress(self):
        '''Updates the progress bar'''
        status = self.client.status()
        if "time" in status:
            current_time, total_time = map(int, status["time"].split(":"))
            progress = int((current_time / total_time) * 100)
            self.progress_bar.setValue(progress)
            self.progress_bar.setFormat(
                f"{strftime(
                    '%M:%S', localtime(current_time))} / {strftime('%M:%S', localtime(total_time)
                    )}"
                )
        else:
            self.progress_bar.setValue(0)

    def scroll_text(self):
        '''Scroll the text inside the song display'''
        try:
            cursor_position = self.song_display.cursorPosition()
            if cursor_position == len(self.current_song):
                if not self.delay_active:
                    self.delay_active = True
                    QTimer.singleShot(3000, self.reset_cursor)
            else:
                self.song_display.setCursorPosition(cursor_position + 1)
        except Exception as e:
            print("There was an error scrolling the text: ", e)

    def reset_cursor(self):
        '''Set the cursor to the start of the line in the song display'''
        self.delay_active = False
        self.song_display.setCursorPosition(0)

    # Buttons
    def on_play_toggle(self, checked):
        '''Update display and mpd playstate'''
        if checked:
            self.playstate = "Playing:"
            self.client.play()
            self.song_changed()
            self.run_user_command("resumed")
        else:
            self.playstate = "Paused:"
            self.client.pause()
            self.song_changed()
            self.run_user_command("paused")

    def on_next_press(self):
        '''Skip current song and update display'''
        try:
            self.client.next()
            # Set the playstate and button to "play"
            if self.mpd_status.get("state") != "play":
                self.toggle.setChecked(True)
                self.playstate = "Playing:"
        except Exception as e:
            print("An error occurred while executing next song command:", e)

    def on_prev_press(self):
        '''Rewind or go back a song and update display'''
        try:
            self.client.previous()
            # Set the playstate and play button to "play"
            if self.mpd_status.get("state") != "play":
                self.toggle.setChecked(True)
                self.playstate = "Playing:"
        except Exception as e:
            print("An error occurred while executing previous song command:", e)

    def on_stop_press(self):
        '''Stop music and update display'''
        self.client.stop()
        self.song_display.setText("Not Playing!")
        self.toggle.setChecked(False)
        self.run_user_command("stopped")

    def closeEvent(self, event): # pylint: disable=invalid-name,unused-argument
        ''''Exit pyamp gracefully'''
        # Close custom command ran by user if it is still open
        if self.user_command:
            if subprocess_instance and subprocess_instance.poll() is None:
                subprocess_instance.terminate()
        # Print the number of songs played
        print("Songs played:", self.songs_played)
        # Close mpd connection
        self.client.disconnect()
        # Stop timers
        self.progress_timer.stop()
        self.scroll_timer.stop()
        self.clock_timer.stop()
        self.check_song_change_timer.stop()
        # Quit qt
        qApp.quit()  # pylint: disable=undefined-variable

    def open_song_picker(self):
        '''Open song picker window'''
        self.song_picker_window.clear_selection()
        self.song_picker_window.show()
        self.song_picker_window.window_close.connect(self.song_changed)

    def update_clock_timer(self):
        '''Calculate the time till the next clock update'''
        # Get the current time
        current_time = localtime()
        # Calculate remaining seconds until next minute
        remaining_seconds = 60 - current_time.tm_sec
        self.clock_timer.setInterval(remaining_seconds * 1000)

    def clock_update(self):
        '''Update the clock'''
        self.current_time = strftime("%H:%M")
        self.clock_display.setText(self.current_time)

    def paintEvent(self, event): # pylint: disable=invalid-name,unused-argument
        '''Draw the window with a background image'''
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_image)
