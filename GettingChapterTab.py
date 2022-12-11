import os

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import (QButtonGroup, QGridLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QSpinBox,
                             QWidget)

from common import *
from SupportFunction import *


class GettingChapterTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout()

        self.setLayout(self.layout)

        self.GC_common_str = {
            "lb_link": "Link: ",
            "rb_nettruyen": "nettruyen",
            "rb_mangasee": "mangasee",
            "lb_server": "Server: ",
            "lb_keyword": "Keyword: "
        }

        self.GC_lb_main_title = QLabel(tabs["GC"])
        self.GC_lb_main_title.setStyleSheet(
            common_font["bold"]+common_color["success"]+font["title"])
        self.layout.addWidget(
            self.GC_lb_main_title, 0, 0, 1, 4, alignment=Qt.AlignCenter)

        self.GC_lb_link = QLabel(self.GC_common_str["lb_link"])
        self.GC_lb_link.setStyleSheet(
            common_font["bold"]+common_color["info"])
        self.layout.addWidget(self.GC_lb_link, 1, 0)

        self.GC_tb_link = QLineEdit()
        self.layout.addWidget(self.GC_tb_link, 1, 1, 1, 3)

        self.GC_rb_nettruyen = QRadioButton(
            text=self.GC_common_str["rb_nettruyen"])

        self.GC_rb_nettruyen.setChecked(True)
        self.GC_rb_mangasee = QRadioButton(
            text=self.GC_common_str["rb_mangasee"])

        self.GC_bg = QButtonGroup()
        self.GC_bg.addButton(self.GC_rb_nettruyen)
        self.GC_bg.addButton(self.GC_rb_mangasee)

        self.GC_lb_server = QLabel(self.GC_common_str["lb_server"])
        self.GC_lb_server.setStyleSheet(
            common_font["bold"]+common_color["info"])
        self.layout.addWidget(self.GC_lb_server, 2, 0)

        self.layout.addWidget(self.GC_rb_nettruyen, 2, 1)
        self.layout.addWidget(
            self.GC_rb_mangasee, 2, 2, 1, 2, alignment=Qt.AlignCenter)

        self.GC_lb_keyword = QLabel(self.GC_common_str["lb_keyword"])
        self.GC_lb_keyword.setStyleSheet(
            common_font["bold"]+common_color["info"])
        self.layout.addWidget(self.GC_lb_keyword, 3, 0)

        self.GC_tb_keyword = QLineEdit()
        self.layout.addWidget(self.GC_tb_keyword, 3, 1, 1, 3)

        self.GC_rb_nettruyen.toggled.connect(
            lambda: self.GC_tb_keyword.setEnabled(self.GC_rb_nettruyen.isChecked()))
