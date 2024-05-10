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
from pyamp.images import BACKGROUND, NEXT, PREV, TOGGLE, ALBUM, STOP, ADD


# Main window
class MainWindow(QMainWindow):
    '''Defines the main window'''
    # Define the song changed signal for the album cover display
    songChanged = Signal()

    def __init__(self, mpd_manager):
        super().__init__()

        # Window title and geometry
        self.setWindowTitle("Pyamp")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 400, 160)
        self.setFixedSize(self.size())

        # Window background and alpha channel
        # Decode the base64 image data
        background_data = base64.b64decode(BACKGROUND)

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

        # MPD and clock stuff/variables
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
        self.title_bar = createTitleBar(self, "Pyamp 0.1.1", button=True)
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
        self.clock_display.setStyleSheet("""
        QLabel {
        font-size: 22pt;
        color: white;
        margin: 10px;
}
""")
        self.clock_display.setText(self.current_time)
        self.clock_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.display_container_layout.addWidget(self.clock_display)
        self.display_container_layout.insertWidget(0, self.clock_display)

        # Timer for updating the clock display in realtime.
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.clock_update)

        # Song display
        self.song_display = NonSelectableLineEdit(central_widget)
        self.song_display.setStyleSheet("""
    QLineEdit {
        border: 1px solid dodgerblue;
        border-radius: 0px;
        background-color: black;
        padding: 2px;
        color: dodgerblue;
}
""")
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
        self.progress_bar.setStyleSheet("""
    QProgressBar {
        border: none;
        background-color: transparent;
        color: dodgerblue;
        text-align: center;
        font-size: 9pt;
    }

    QProgressBar::chunk {
        background-color: black;
        border: 1px solid dodgerblue;
    }
""")
        self.progress_bar.setFixedHeight(20)
        self.song_container_layout.addWidget(self.progress_bar)

        # Timer to update progress bar periodically
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress)

        # Volume slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setFixedHeight(15)
        self.volume_slider.setStyleSheet("""
    QSlider::groove:horizontal {
        background-color: black;
        border: 1px solid dodgerblue;
    }

    QSlider::handle:horizontal {
        background-color: #262626;
        border: 1px solid dodgerblue;
        margin: -4 0;
        width: 10px;
    }
    QSlider::handle:horizontal::active {
        border-width: 3px;
    }
""")
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
        button_stylesheet = """
            QPushButton{
                background-color: black;
                border: 1px solid dodgerblue;
            }
            QPushButton:hover{
                background-color: black;
                border: 2px solid dodgerblue;
            }
            QPushButton:pressed{
                background-color: transparent;
            }
            QPushButton:checked {
                background-color: transparent;
            }
        """

        # Previous song button
        prev_icon = QIcon(QPixmap.fromImage(QImage.fromData(base64.b64decode(PREV))))
        self.prev = QPushButton("", self)
        self.prev.setFixedHeight(25)
        self.prev.setFixedWidth(25)
        self.button_container_layout.addWidget(self.prev)
        self.prev.setIcon(prev_icon)
        self.prev.setStyleSheet(button_stylesheet)
        self.prev.clicked.connect(self.on_prev_press)

        # Stop button
        stop_icon = QIcon(QPixmap.fromImage(QImage.fromData(base64.b64decode(STOP))))
        self.stop = QPushButton("", self)
        self.stop.setFixedHeight(25)
        self.stop.setFixedWidth(25)
        self.button_container_layout.addWidget(self.stop)
        self.stop.setIcon(stop_icon)
        self.stop.setStyleSheet(button_stylesheet)
        self.stop.clicked.connect(self.on_stop_press)

        # Play/Pause button
        toggle_icon = QIcon(QPixmap.fromImage(QImage.fromData(base64.b64decode(TOGGLE))))
        self.toggle = QPushButton("", self)
        self.toggle.setCheckable(True)
        self.toggle.setFixedHeight(25)
        self.toggle.setFixedWidth(25)
        self.button_container_layout.addWidget(self.toggle)
        self.toggle.setIcon(toggle_icon)
        self.toggle.setStyleSheet(button_stylesheet)
        self.toggle.clicked.connect(self.on_play_toggle)

        # Song picker button
        add_icon = QIcon(QPixmap.fromImage(QImage.fromData(base64.b64decode(ADD))))
        self.add = QPushButton("", self)
        self.add.setFixedHeight(25)
        self.add.setFixedWidth(25)
        self.button_container_layout.addWidget(self.add)
        self.add.setIcon(add_icon)
        self.add.setStyleSheet(button_stylesheet)
        self.song_picker_window = SongPickerWindow(mpd_manager)
        self.add.clicked.connect(self.open_song_picker)

        # Next song button
        next_icon = QIcon(QPixmap.fromImage(QImage.fromData(base64.b64decode(NEXT))))
        self.next = QPushButton("", self)
        self.next.setFixedHeight(25)
        self.next.setFixedWidth(25)
        self.button_container_layout.addWidget(self.next)
        self.next.setIcon(next_icon)
        self.next.setStyleSheet(button_stylesheet)
        self.next.clicked.connect(self.on_next_press)

        # Album art button
        album_icon = QIcon(QPixmap.fromImage(QImage.fromData(base64.b64decode(ALBUM))))
        self.album = QPushButton("", self)
        self.album.setFixedHeight(25)
        self.album.setFixedWidth(25)
        self.button_container_layout.addWidget(self.album)
        self.album.setIcon(album_icon)
        self.album.setStyleSheet(button_stylesheet)
        self.album_display = AlbumCoverWindow(mpd_manager, self)
        self.album.clicked.connect(self.open_album_display)

        # Timer checking for song changes
        self.check_song_change_timer = QTimer(self)
        self.check_song_change_timer.timeout.connect(self.check_song_change)
        self.previous_song = None

        # Skibidi rizz
        self.startup()

    def startup(self):
        '''Runs/Starts all the music related functions'''
        # Checks mpd status
        if self.mpd_status.get("state") == "play":
            # Sets status and button to "play"
            self.toggle.setChecked(True)
            self.playstate = "Playing:"
        elif self.mpd_status.get("state") == "pause":
            # Sets status and button to "pause"
            self.toggle.setChecked(False)
            self.playstate = "Paused:"
        else:
            self.playstate = "Not Playing!"
        # Essentially starts the song and clock related stuff
        self.song_changed()
        self.check_song_change_timer.start(1000)
        self.scroll_timer.start(80)
        self.progress_timer.start(1000)
        self.update_clock_timer()
        self.clock_timer.start()

    def check_song_change(self):
        '''Checks for a song change and runs additional functions if it detects one'''
        try:
            # Check for song change
            current_song = self.client.currentsong()
            if current_song != self.previous_song:
                # Updates the current song info
                self.previous_song = current_song
                self.songChanged.emit()

                # Runs run_on_song_change command if there's one
                if self.user_command:
                    try:
                        global subprocess_instance
                        with subprocess.Popen(self.user_command.split()) as subprocess_instance:
                            subprocess_instance.communicate()
                    except Exception as e:
                        print("An error ocurred while running the custom command: ", e)

                # Skips the first current song var update
                if self.songs_played == 0:
                    # If no song has played yet, increment the counter by 1
                    self.songs_played += 1
                else:
                    # Updates the song display
                    self.song_changed()
                    # Increments the songs played counter on every song change
                    self.songs_played += 1

        except Exception as e:
            print("Connection error:", e)
            self.close()

    def get_current_song_info(self):
        '''Gets all the current song info'''
        try:
            status = self.client.status()
            if status.get("state") == "stop":
                # Sets the current song variable
                self.current_song = "Not Playing!"
            else:
                # Fetches MPD's current song info
                current_song_info = self.client.currentsong()

                # Sets the current song variable
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

            # Returns the current song variable
            return self.current_song
        except Exception as e:
            print(f"An error occurred while getting current song info: {e}")
            return None

    def song_changed(self):
        '''Updates the current song and displays it.'''
        state = self.mpd_status.get("state")
        if state in ["play", "pause", "stop"]:
            self.current_song = self.get_current_song_info()
            self.song_display.setText(self.current_song)
            self.song_display.setCursorPosition(0)
        else:
            self.current_song = "Not Playing!"
            self.song_display.setText(self.current_song)
            self.song_display.setCursorPosition(0)
            # Redundant code ^^^

    def get_slider_value(self):
        '''Returns MPD's volume. If MPD isn't playing returns 50'''
        try:
            if self.mpd_status.get("state") != "stop":
                slider_value = int(self.client.status()["volume"])
            else:
                slider_value = 50
        except Exception:
            slider_value = 50
        return slider_value

    def volume_changed(self, value):
        '''Changes mpd's volume if the volume slider is changed'''
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
        '''Scrolls song display text'''
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
        '''Resets the cursor to the start of the line'''
        self.delay_active = False
        self.song_display.setCursorPosition(0)

    # Buttons
    def on_play_toggle(self, checked):
        '''Alters the play state based on self.play check state'''
        if checked:
            self.playstate = "Playing:"
            self.client.play()
            self.song_changed()
        else:
            self.playstate = "Paused:"
            self.client.pause()
            self.song_changed()

    def on_next_press(self):
        '''Skips song and changes play state'''
        try:
            self.client.next()
            # Sets the playstate and button to "play"
            if self.mpd_status.get("state") != "play":
                self.toggle.setChecked(True)
                self.playstate = "Playing:"
        except Exception as e:
            print("An error occurred while executing next song command:", e)

    def on_prev_press(self):
        '''Rewinds song and changes play state'''
        try:
            self.client.previous()
            # Sets the playstate and button to "play"
            if self.mpd_status.get("state") != "play":
                self.toggle.setChecked(True)
                self.playstate = "Playing:"
        except Exception as e:
            print("An error occurred while executing previous song command:", e)

    def on_stop_press(self):
        '''Stops music and changes display text'''
        self.client.stop()
        self.song_display.setText("Not Playing!")
        self.toggle.setChecked(False)

    def closeEvent(self, event): # pylint: disable=invalid-name,unused-argument
        ''''Re-defines closeEvent to properly close the program'''
        # Closes custom command ran by user if it is still open
        if subprocess_instance and subprocess_instance.poll() is None:
            subprocess_instance.terminate()
        # Prints the number of songs played
        print("Songs played:", self.songs_played)
        # Closes mpd connection
        self.client.disconnect()
        # Stops timers
        self.progress_timer.stop()
        self.scroll_timer.stop()
        self.clock_timer.stop()
        self.check_song_change_timer.stop()
        # Quits qt
        qApp.quit()  # pylint: disable=undefined-variable

    def open_song_picker(self):
        '''Opens the song picker'''
        self.song_picker_window.clear_selection()
        self.song_picker_window.show()
        self.song_picker_window.window_close.connect(self.song_changed)

    def open_album_display(self):
        '''Opens the album display'''
        self.album_display.show()

    def update_clock_timer(self):
        '''Runs clock update every minute'''
        # Gets the current time
        current_time = localtime()
        # Calculate remaining seconds until next minute
        remaining_seconds = 60 - current_time.tm_sec
        self.clock_timer.setInterval(remaining_seconds * 1000)

    def clock_update(self):
        '''Updates the clock'''
        self.current_time = strftime("%H:%M")
        self.clock_display.setText(self.current_time)

    def paintEvent(self, event): # pylint: disable=invalid-name,unused-argument
        '''Re-defines the painEvent so the background image actually displays'''
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_image)
        self.delay_active = False
