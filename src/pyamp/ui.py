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
from PySide6.QtWidgets import QLineEdit, QWidget, QPushButton, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt


class CreateSpacer(QSpacerItem):
    def __init__(self, width, height, size_policy_horizontal, size_policy_vertical):
        super().__init__(width, height, size_policy_horizontal, size_policy_vertical)


class NonSelectableLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        event.ignore()

    def mouseMoveEvent(self, event):
        event.ignore()


class createTitleBar(QWidget):
    def __init__(self, parent, title, button=True):
        super().__init__(parent)
        self.title = title
        self.button = button
        self.init_ui()

    def init_ui(self):
        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(5, 4, 5, 0)

        # Title spacer
        title_spacer = QSpacerItem(16, 16, QSizePolicy.Fixed, QSizePolicy.Fixed)
        title_bar_layout.addItem(title_spacer)

        # Title label
        title_label = QLabel(self.title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: dodgerblue;
                font-size: 10px;
            }
        """)
        title_bar_layout.addWidget(title_label)

        # Close button (if enabled)
        if self.button:
            close_button = QPushButton("X")
            close_button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: dodgerblue;
                }
                QPushButton:hover {
                    background-color: dodgerblue;
                    color: black;
                }
                QPushButton:pressed {
                    background-color: dodgerblue;
                    color: white;
                }
            """)
            close_button.setFixedHeight(16)
            close_button.setFixedWidth(16)
            close_button.clicked.connect(self.parent().close)
            title_bar_layout.addWidget(close_button)
