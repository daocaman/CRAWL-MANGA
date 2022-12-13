import os

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import (QButtonGroup, QGridLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QSpinBox,
                             QWidget)

from common import *
from QLabelLink import *
from SupportFunction import *


class GetImageLinkTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout()

        self.setLayout(self.layout)

        self.GI_common_str = {
            "lb_link": "Link: ",
            "btn_create_lf": "Create",
            "lb_server": "Server: ",
            "rb_nettruyen": "Nettruyen",
            "rb_mangasee": "Mangasee",
            "rb_sinhvien": "Sinhvien",
            "lb_result": "Result file: ",
            "btn_get_link": "Get",
            "lb_progress": "Progress: "
        }

        self.GC_lb_main_title = QLabel(tabs["GI"])
        self.GC_lb_main_title.setStyleSheet(
            common_font["bold"]+common_color["success"]+font["title"])
        self.layout.addWidget(
            self.GC_lb_main_title, 0, 0, 1, 4, alignment=Qt.AlignCenter)

        self.GI_lb_link = QLabel(self.GI_common_str["lb_link"])
        self.GI_lb_link.setStyleSheet(common_color["info"]+common_font["bold"])
        self.layout.addWidget(self.GI_lb_link, 1, 0)

        self.GI_lbl_link_file = QLabelLink()
        if os.path.exists("resource/link.txt"):
            self.GI_lbl_link_file.setText("link.txt")
        else:
            self.GI_lbl_link_file.setText("...")
            self.GI_lbl_link_file.setEnabled(False)
        self.layout.addWidget(self.GI_lbl_link_file, 1, 1, 1, 2)

        self.GI_btn_create_lf = QPushButton(
            self.GI_common_str["btn_create_lf"])
        self.GI_btn_create_lf.setStyleSheet(
            btns["default"]+btns["outline-primary"])
        self.layout.addWidget(self.GI_btn_create_lf, 1, 3)

        self.GI_lb_server = QLabel(self.GI_common_str["lb_server"])
        self.GI_lb_server.setStyleSheet(
            common_color["info"]+common_font["bold"])
        self.layout.addWidget(self.GI_lb_server, 2, 0)

        self.GI_btngroup_server = QButtonGroup()

        self.GI_rb_nettruyen = QRadioButton(self.GI_common_str["rb_nettruyen"])
        self.GI_rb_nettruyen.setStyleSheet(common_color["warning"])
        self.GI_btngroup_server.addButton(self.GI_rb_nettruyen)
        self.layout.addWidget(self.GI_rb_nettruyen, 2, 1)

        self.GI_rb_mangasee = QRadioButton(self.GI_common_str["rb_mangasee"])
        self.GI_rb_mangasee.setStyleSheet(common_color["warning"])
        self.GI_btngroup_server.addButton(self.GI_rb_mangasee)
        self.layout.addWidget(self.GI_rb_mangasee, 2, 2)

        self.GI_rb_sinhvien = QRadioButton(self.GI_common_str["rb_sinhvien"])
        self.GI_rb_sinhvien.setStyleSheet(common_color["warning"])
        self.GI_btngroup_server.addButton(self.GI_rb_sinhvien)
        self.layout.addWidget(self.GI_rb_sinhvien, 2, 3)

        self.GI_lb_result = QLabel(self.GI_common_str["lb_result"])
        self.GI_lb_result.setStyleSheet(
            common_color["info"]+common_font["bold"])
        self.layout.addWidget(self.GI_lb_result, 3, 0)

        self.GI_lbl_result_file = QLabelLink()
        self.layout.addWidget(self.GI_lbl_result_file,3, 1)

        self.GI_btn_get_link = QPushButton(self.GI_common_str["btn_get_link"])
        self.GI_btn_get_link.setStyleSheet(btns["default"]+btns["outline-success"])
        self.layout.addWidget(self.GI_btn_get_link,3, 3)

        self.GI_lb_progress = QLabel(self.GI_common_str["lb_progress"])
        self.GI_lb_progress.setStyleSheet(common_color["info"]+ common_font["bold"])

        self.layout.setSpacing(15)
        self.layout.setRowStretch(6, 1)



        
