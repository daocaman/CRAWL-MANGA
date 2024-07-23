import os

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import (QGridLayout, QLabel,
                             QProgressBar, QPushButton, QWidget)
from QLabelLink import *
from common import *
from SupportFunction import *

import subprocess


class DownloadComicURLTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout()

        self.setLayout(self.layout)

        self.DC_common_str = {
            "lb_file": "File: ",
            "rb_nettruyen": "nettruyen",
            "btn_download": "Download",
            "lb_progress": "Progress: "
        }

        self.DC_lb_main_title = QLabel(tabs["DC"]['l'])
        self.DC_lb_main_title.setStyleSheet(generateStyle({**font_bold, **text_success, **font_title}))
        self.layout.addWidget(
            self.DC_lb_main_title, 0, 0, 1, 4, alignment=Qt.AlignCenter)

        self.DC_lb_file = QLabel(self.DC_common_str["lb_file"])
        self.DC_lb_file.setStyleSheet(generateStyle({**font_bold, **text_info}))
        self.layout.addWidget(self.DC_lb_file, 1, 0)

        self.DC_lbl_file = QLabelLink()
        self.layout.addWidget(self.DC_lbl_file, 1, 1, 1, 3)

        if os.path.exists('resource/chapter.json'):
            self.DC_lbl_file.setText('chapter.json')
        else:
            self.DC_lbl_file.setText('...')
            self.DC_lbl_file.setEnabled(False)

        self.DC_lbl_file.clicked.connect(
            lambda: subprocess.run(['start', 'resource/chapter.json'], shell=True))

        self.DC_lb_progress = QLabel(self.DC_common_str["lb_progress"])
        self.DC_lb_progress.setStyleSheet(generateStyle({**font_bold, **text_info}))
        self.layout.addWidget(self.DC_lb_progress, 2, 0)

        self.DC_progress_down = QProgressBar()
        self.DC_progress_down.setValue(0)
        self.layout.addWidget(self.DC_progress_down, 2, 1, 1, 3)

        self.DC_lb_progress_txt = QLabel()
        self.DC_lb_progress_txt.setStyleSheet(generateStyle({**font_bold, **text_warning}))
        self.layout.addWidget(self.DC_lb_progress_txt, 3, 0, 1, 3)

        self.DC_btn_download = QPushButton(self.DC_common_str["btn_download"])
        self.DC_btn_download.setStyleSheet(generateStyle(btn_danger))
        self.layout.addWidget(self.DC_btn_download, 3, 3)

        self.layout.setSpacing(15)
        self.layout.setRowStretch(4, 1)

        self.DC_btn_download.clicked.connect(self.DC_download)

    def DC_download(self):
        self.DC_thread = QThread()

        self.worker = DownloadImage()

        self.worker.moveToThread(self.DC_thread)

        self.DC_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.DC_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.DC_thread.finished.connect(self.DC_thread.deleteLater)
        self.worker.progress.connect(self.DC_updateProgress)

        self.DC_thread.start()

        self.worker.finished.connect(self.DC_finish_download)

    def DC_updateProgress(self, data):
        self.DC_progress_down.setValue(data[1])
        if data[0] != "":
            self.DC_lb_progress_txt.setText(data[0])

    def DC_finish_download(self, data):
        if data[1] == 200:
            n.show_toast(msg["suc_dc"]["t"], msg["suc_dc"]
                         ["m"], duration=2, threaded=True)
        else:
            self.DC_lb_progress_txt.setText(data[0])
            n.show_toast('Error', 'Please check all condition!!!',
                         duration=2, threaded=True)
