import base64
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QGridLayout,
    QLabel,
    QVBoxLayout
)
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt


class OptionsWindow(QMainWindow):
    '''Creates a window for changing MPD's playback options'''

    def __init__(self, mpd_manager, img_op_background, options_stylesheet):
        super().__init__()

        # Window title and geometry
        self.setWindowTitle("Options")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 160, 160)
        self.setFixedSize(self.size())

        # Central widget config
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout config
        self.layout = QGridLayout(central_widget)
        central_widget.setLayout(self.layout)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setAlignment(Qt.AlignCenter)


        # Window background and alpha channel
        # Decode the base64 image data
        background_data = base64.b64decode(img_op_background)

        # Create a QPixmap from the binary data
        background_pixmap = QPixmap()
        background_pixmap.loadFromData(background_data)

        # Set the background image and mask
        self.background_image = background_pixmap
        self.setMask(self.background_image.mask())

        # Stylesheet
        self.stylesheet = options_stylesheet

        # MPD Stuff
        self.client = mpd_manager.get_client()
        self.client_status = self.client.status()

        # Window Label
        label = QLabel("Playback Options")
        label.setStyleSheet(self.stylesheet)
        self.layout.addWidget(label)

        # Buttons Container
        self.button_container = QWidget()
        self.button_container_layout = QVBoxLayout(self.button_container)
        self.button_container_layout.setContentsMargins(0, 5, 0, 0)
        self.layout.addWidget(self.button_container)
        self.button_container_layout.setAlignment(Qt.AlignCenter)

        self.rnd_button = QPushButton("Random")
        self.button_container_layout.addWidget(self.rnd_button)
        self.rnd_button.setFixedHeight(25)
        self.rnd_button.setFixedWidth(100)
        self.rnd_button.setCheckable(True)
        self.rnd_button.clicked.connect(lambda: self.button_action(self.client.random, self.rnd_button, "random", "toggle"))
        self.button_action(self.client.random, self.rnd_button, "random", "check")
        self.rnd_button.setStyleSheet(self.stylesheet)

        self.consume_button = QPushButton("Consume")
        self.button_container_layout.addWidget(self.consume_button)
        self.consume_button.setFixedHeight(25)
        self.consume_button.setFixedWidth(100)
        self.consume_button.setCheckable(True)
        self.consume_button.clicked.connect(lambda: self.button_action(self.client.consume, self.consume_button, "Consume", "toggle"))
        self.button_action(self.client.consume, self.consume_button, "consume", "check")
        self.consume_button.setStyleSheet(self.stylesheet)

        self.single_button = QPushButton("Single")
        self.button_container_layout.addWidget(self.single_button)
        self.single_button.setFixedHeight(25)
        self.single_button.setFixedWidth(100)
        self.single_button.setCheckable(True)
        self.single_button.clicked.connect(lambda: self.button_action(self.client.single, self.single_button, "Single", "toggle"))
        self.button_action(self.client.single, self.single_button, "single", "check")
        self.single_button.setStyleSheet(self.stylesheet)

        self.rpt_button = QPushButton("Repeat")
        self.button_container_layout.addWidget(self.rpt_button)
        self.rpt_button.setFixedHeight(25)
        self.rpt_button.setFixedWidth(100)
        self.rpt_button.setCheckable(True)
        self.rpt_button.clicked.connect(lambda: self.button_action(self.client.repeat, self.rpt_button, "Repeat", "toggle"))
        self.button_action(self.client.repeat, self.rpt_button, "repeat", "check")
        self.rpt_button.setStyleSheet(self.stylesheet)

        self.installEventFilter(self)

    def button_action(self, command, button, text, mode):
        '''Changes the button's check state, label and/or changes MPD's playback options'''
        if mode == "check":
            state = self.client_status.get(text)
            if state == "1":
                button.setChecked(1)
                label = text[0].upper() + text[1:]
                button.setText(f"{label} ON")
            elif state == "0":
                button.setChecked(0)
                label = text[0].upper() + text[1:]
                button.setText(f"{label} OFF")
        elif mode == "toggle":
            if button.isChecked():
                command(1)
                label = text[0].upper() + text[1:]
                button.setText(f"{label} ON")
            else:
                command(0)
                label = text[0].upper() + text[1:]
                button.setText(f"{label} OFF")
        else:
            self.close()

    def keyPressEvent(self, event): # pylint: disable=C0103
        '''Closes the window on q or escape key press'''
        if event.key() == Qt.Key_Q or event.key() == Qt.Key_Escape:
            self.close()

    def paintEvent(self, event): # pylint: disable=invalid-name,unused-argument
        '''Re-defines the painEvent so the background image actually displays'''
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_image)
