import os

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (QButtonGroup, QGridLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QSpinBox,
                             QWidget)

from common import *
from SupportFunction import *



class QLabelLink(QLabel):

    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setStyleSheet(common_font["underline"]+common_color["primary"])

    def mousePressEvent(self, event):
        self.clicked.emit()
