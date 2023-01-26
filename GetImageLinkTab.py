import os

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import (QComboBox, QGridLayout, QLabel, QLineEdit,
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
            "lb_keyword": "Keyword",
            "lb_result": "Result file: ",
            "btn_get_link": "Get",
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

        self.GI_sb_server = QComboBox()
        self.GI_sb_server.addItems(["nettruyen", "mangasee", "sinhvien"])
        self.layout.addWidget(self.GI_sb_server, 2, 1, 1, 3)

        self.GI_lb_keyword = QLabel(self.GI_common_str["lb_keyword"])
        self.GI_lb_keyword.setStyleSheet(
            common_color["info"]+common_font["bold"])
        self.layout.addWidget(self.GI_lb_keyword, 3, 0)

        self.GI_tb_keyword = QLineEdit()
        self.layout.addWidget(self.GI_tb_keyword, 3, 1, 1, 3)
        self.GI_tb_keyword.setEnabled(False)

        self.GI_lb_result = QLabel(self.GI_common_str["lb_result"])
        self.GI_lb_result.setStyleSheet(
            common_color["info"]+common_font["bold"])
        self.layout.addWidget(self.GI_lb_result, 4, 0)

        self.GI_lbl_result_file = QLabelLink()
        self.layout.addWidget(self.GI_lbl_result_file, 4, 1, 1, 2)
        self.GI_lbl_result_file.setEnabled(False)

        self.GI_btn_get_link = QPushButton(self.GI_common_str["btn_get_link"])
        self.GI_btn_get_link.setStyleSheet(
            btns["default"]+btns["outline-success"])
        self.layout.addWidget(self.GI_btn_get_link, 4, 3)

        self.GI_progress_down = QProgressBar()
        self.GI_progress_down.setValue(0)
        self.layout.addWidget(self.GI_progress_down, 5, 0, 1, 4)

        self.GI_progress_txt = QLabel()
        self.GI_progress_txt.setStyleSheet(
            common_color["warning"]+common_font["bold"])
        self.layout.addWidget(self.GI_progress_txt, 6, 0, 1, 4)

        self.GI_sb_server.currentIndexChanged.connect(self.GI_changeServer)

        self.GI_btn_get_link.clicked.connect(self.GI_getImgSrc)

        self.GI_lbl_link_file.clicked.connect(lambda: os.system('code ' + 'resource/link.txt'))
        self.GI_lbl_result_file.clicked.connect(lambda: os.system('code ' + 'resource/chapters.txt'))

        self.layout.setSpacing(15)
        self.layout.setRowStretch(6, 1)

    def GI_changeServer(self, value):
        self.GI_tb_keyword.setEnabled(value == 1)
    
    def GI_getImgSrc(self):
        self.GI_refresh()
        self.GI_thread = QThread()

        self.worker = GetImageSrc(self.GI_sb_server.currentIndex(),self.GI_tb_keyword.text())

        self.worker.moveToThread(self.GI_thread)

        self.GI_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.GI_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.GI_thread.finished.connect(self.GI_thread.deleteLater)
        self.worker.progress.connect(self.GI_updateProgress)

        self.GI_thread.start()

        self.worker.finished.connect(self.GI_finish_getting)
    
    def GI_finish_getting(self, value):
        if value == -1:
            n.show_toast(msg["err_di_er"]["t"], msg["err_di_er"]
                     ["m"], duration=2, threaded=True)
        elif value == 401:
            n.show_toast(msg["err_di_401"]["t"], msg["err_di_401"]
                     ["m"], duration=2, threaded=True)
        else:
            n.show_toast(msg["suc_di"]["t"], msg["suc_di"]
                     ["m"], duration=2, threaded=True)

            self.GI_lbl_result_file.setText("chapters.txt")
            self.GI_lbl_result_file.setEnabled(True)

    def GI_updateProgress(self, data):
        self.GI_progress_txt.setText(data[0])
        self.GI_progress_down.setValue(data[1])

    def GI_refresh(self):
        self.GI_lbl_result_file.setText("")
        self.GI_lbl_result_file.setEnabled(False)
        self.GI_progress_down.setValue(0)
