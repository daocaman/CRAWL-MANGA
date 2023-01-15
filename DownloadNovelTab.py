import os

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import (QGridLayout, QLabel, QLineEdit, QComboBox,
                             QProgressBar, QPushButton, QWidget, QSpinBox)
from QLabelLink import *
from common import *
from SupportFunction import *


class DownloadNovelTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout(self)

        self.DV_common_str = {
            "lb_link": "Link: ",
            "lb_novel_name": "Novel name: ",
            "lb_start_chap": "From chap: ",
            "lb_end_chap": "To chap: ",
            "lb_result": "Resut file: ",
            "btn_download": "Download",
            "lb_server": "Servers: "
        }

        self.DV_lb_main_title = QLabel(tabs["DV"])
        self.DV_lb_main_title.setStyleSheet(
            common_font["bold"]+common_color["success"]+font["title"])
        self.layout.addWidget(
            self.DV_lb_main_title, 0, 0, 1, 4, alignment=Qt.AlignCenter)

        self.DV_lb_link = QLabel(self.DV_common_str["lb_link"])
        self.DV_lb_link.setStyleSheet(common_font["bold"]+common_color["info"])
        self.layout.addWidget(self.DV_lb_link, 1, 0)

        self.DV_tb_link = QLineEdit()
        self.layout.addWidget(self.DV_tb_link, 1, 1, 1, 3)

        self.DV_lb_server = QLabel(self.DV_common_str["lb_server"])
        self.DV_lb_server.setStyleSheet(common_font["bold"]+common_color["info"])
        self.layout.addWidget(self.DV_lb_server, 2, 0)

        self.DV_sb_server = QComboBox()
        self.DV_sb_server.addItems(["metruyencv", "sstruyen", "trumtruyen"])
        self.layout.addWidget(self.DV_sb_server, 2, 1, 1, 3)


        self.DV_lb_novel_name = QLabel(self.DV_common_str["lb_novel_name"])
        self.DV_lb_novel_name.setStyleSheet(
            common_font["bold"]+common_color["info"])
        self.layout.addWidget(self.DV_lb_novel_name, 3, 0)

        self.DV_tb_novel_name = QLineEdit()
        self.layout.addWidget(self.DV_tb_novel_name, 3, 1, 1, 3)

        self.DV_lb_start_chap = QLabel(self.DV_common_str["lb_start_chap"])
        self.DV_lb_start_chap.setStyleSheet(
            common_font["bold"]+common_color["info"])
        self.layout.addWidget(self.DV_lb_start_chap, 4, 0)

        self.DV_spb_start_chap = QSpinBox()
        self.DV_spb_start_chap.setValue(1)
        self.DV_spb_start_chap.setMinimum(1)
        self.DV_spb_start_chap.setMaximum(10000)
        self.layout.addWidget(self.DV_spb_start_chap, 4, 1)

        self.DV_lb_end_chap = QLabel(self.DV_common_str["lb_end_chap"])
        self.DV_lb_end_chap.setStyleSheet(
            common_font["bold"]+common_color["info"])
        self.layout.addWidget(self.DV_lb_end_chap, 4, 2)

        self.DV_spb_end_chap = QSpinBox()
        self.DV_spb_end_chap.setValue(1)
        self.DV_spb_end_chap.setMinimum(1)
        self.DV_spb_end_chap.setMaximum(10000)
        self.layout.addWidget(self.DV_spb_end_chap, 4, 3)

        self.DV_lb_result = QLabel(self.DV_common_str["lb_result"])
        self.DV_lb_result.setStyleSheet(
            common_font["bold"]+common_color["info"])
        self.layout.addWidget(self.DV_lb_result, 5, 0)

        self.DV_lb_file_name = QLabelLink("")
        self.DV_lb_file_name.setStyleSheet(
            common_font["underline"]+common_color["primiary"])
        self.DV_lb_file_name.setEnabled(False)
        self.layout.addWidget(self.DV_lb_file_name, 5, 1, 1, 2)

        self.DV_btn_download = QPushButton(self.DV_common_str["btn_download"])
        self.DV_btn_download.setStyleSheet(btns["default"]+btns["danger"])
        self.DV_btn_download.setEnabled(False)
        self.layout.addWidget(self.DV_btn_download, 5, 3)

        self.DV_progress_down = QProgressBar()
        self.DV_progress_down.setValue(0)
        self.layout.addWidget(self.DV_progress_down, 6, 0, 1, 4)

        self.DV_lb_progress = QLabel()
        self.DV_lb_progress.setStyleSheet(common_color["warning"])
        self.layout.addWidget(self.DV_lb_progress, 7, 0, 1, 4)

        self.layout.setSpacing(15)
        self.layout.setRowStretch(8, 1)

        self.DV_tb_link.textChanged.connect(self.DV_updateState)
        self.DV_tb_novel_name.textChanged.connect(self.DV_updateState)

        self.DV_btn_download.clicked.connect(self.DV_downloadNovel)
        self.DV_lb_file_name.clicked.connect(self.DV_openFolder)

        self.setLayout(self.layout)

    def DV_updateState(self, newStr):
        if "http" in self.DV_tb_link.text() and self.DV_tb_novel_name.text() != "":
            self.DV_btn_download.setEnabled(True)

    def DV_downloadNovel(self):
        self.DV_thread = QThread()

        self.worker = DownloadNovel(self.DV_tb_link.text(), self.DV_spb_start_chap.value(
        ), self.DV_spb_end_chap.value(), self.DV_tb_novel_name.text(), self.DV_sb_server.currentIndex())

        self.worker.moveToThread(self.DV_thread)

        self.DV_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.DV_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.DV_thread.finished.connect(self.DV_thread.deleteLater)
        self.worker.progress.connect(self.DV_updateProgress)

        self.DV_thread.start()

        self.worker.finished.connect(self.DV_finish_download)

    def DV_openFolder(self):
        os.system("start " + "resource")

    def DV_updateProgress(self, data):
        self.DV_lb_progress.setText(data[0])
        self.DV_progress_down.setValue(data[1])

    def DV_finish_download(self, filename):
        self.DV_lb_file_name.setEnabled(True)
        self.DV_lb_file_name.setText(filename)

        n.show_toast(msg["suc_dv"]["t"], msg["suc_dv"]
                     ["m"], duration=2, threaded=True)
