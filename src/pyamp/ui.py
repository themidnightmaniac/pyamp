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
from PySide6.QtWidgets import (
    QLineEdit,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QSpacerItem,
    QSizePolicy
)
from PySide6.QtCore import Qt

class CreateSpacer(QSpacerItem):
    '''Creates a spacer item'''
    def __init__(self, width, height, size_policy_horizontal, size_policy_vertical): # pylint: disable=W0246
        super().__init__(width, height, size_policy_horizontal, size_policy_vertical)


class NonSelectableLineEdit(QLineEdit):
    '''Creates a non selectable textbox'''
    def __init__(self, *args, **kwargs): # pylint: disable=W0246
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event): # pylint: disable=C0103
        '''Redefines the mouse press event so nothing happens when clicked'''
        event.ignore()

    def mouseMoveEvent(self, event): # pylint: disable=C0103
        '''Redefines the mouse move event so nothing happens when the cursor is moved'''
        event.ignore()


class createTitleBar(QWidget): # pylint: disable=C0103
    '''Creates a title bar'''
    def __init__(self, parent, title, tbar_stylesheet, button=True):
        super().__init__(parent)
        self.title = title
        self.button = button
        self.stylesheet = tbar_stylesheet
        self.init_ui()

    def init_ui(self):
        '''Creates the title bar'''
        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(5, 4, 5, 0)
        # Close button (if enabled)
        if self.button:
            more_button = QPushButton("=")
            more_button.setStyleSheet(self.stylesheet)
            more_button.setFixedHeight(16)
            more_button.setFixedWidth(16)
            more_button.clicked.connect(lambda: print("Clicked"))
            title_bar_layout.addWidget(more_button)

            title_label = QLabel(self.title)
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setStyleSheet(self.stylesheet)
            title_bar_layout.addWidget(title_label)

            close_button = QPushButton("X")
            close_button.setStyleSheet(self.stylesheet)
            close_button.setFixedHeight(16)
            close_button.setFixedWidth(16)
            close_button.clicked.connect(self.parent().close)
            title_bar_layout.addWidget(close_button)
        else:
            spacer = QSpacerItem(16, 16, QSizePolicy.Fixed, QSizePolicy.Fixed)
            title_bar_layout.addItem(spacer)
            # Title label
            title_label = QLabel(self.title)
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setStyleSheet(self.stylesheet)
            title_bar_layout.addWidget(title_label)
