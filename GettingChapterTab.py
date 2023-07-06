import os

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import (QButtonGroup, QGridLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QFileDialog,
                             QWidget)

from common import *
from SupportFunction import *
from QLabelLink import *
import subprocess
import shutil


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
            "lb_result": "Result file: ",
            "btn_get_chapter": "Get",
            "lb_progress": "Progress: ",
            "lb_previous_chapters": "Previous download: ",
            "btn_get_prev": "Find"
        }

        self.GC_lb_main_title = QLabel(tabs["GC"]["l"])
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
        self.layout.addWidget(self.GC_rb_mangasee, 2, 2,
                              1, 2, alignment=Qt.AlignCenter)

        self.GC_lb_previous = QLabel(
            self.GC_common_str['lb_previous_chapters'])
        self.GC_lb_previous.setStyleSheet(
            common_font["bold"]+common_color["info"])
        self.layout.addWidget(self.GC_lb_previous, 3, 0)

        self.GC_tb_file_chapters = QLineEdit()
        self.layout.addWidget(self.GC_tb_file_chapters, 3, 1, 1, 2)

        self.GC_tb_file_chapters.setReadOnly(True)

        self.GC_btn_find = QPushButton(self.GC_common_str['btn_get_prev'])
        self.GC_btn_find.setStyleSheet(btns["default"]+btns["success"])
        self.layout.addWidget(self.GC_btn_find, 3, 3, 1, 1)

        self.GC_lb_result = QLabel(self.GC_common_str["lb_result"])
        self.GC_lb_result.setStyleSheet(
            common_color["info"]+common_font["bold"])
        self.layout.addWidget(self.GC_lb_result, 4, 0)

        self.GC_lb_result_file = QLabelLink()
        self.GC_lb_result_file.setEnabled(False)
        self.layout.addWidget(self.GC_lb_result_file, 4, 1)

        self.GC_btn_get_chapter = QPushButton(
            self.GC_common_str["btn_get_chapter"])
        self.GC_btn_get_chapter.setStyleSheet(btns["default"]+btns["primary"])
        self.layout.addWidget(self.GC_btn_get_chapter, 4, 3)

        self.GC_lb_progress = QLabel(self.GC_common_str["lb_progress"])
        self.GC_lb_progress.setStyleSheet(
            common_color["info"]+common_font["bold"])
        self.layout.addWidget(self.GC_lb_progress, 5, 0)

        self.GC_progress_getting = QProgressBar()
        self.GC_progress_getting.setValue(0)
        self.layout.addWidget(self.GC_progress_getting, 5, 1, 1, 3)

        self.GC_lb_progress_msg = QLabel()
        self.GC_lb_progress_msg.setStyleSheet(
            common_color["warning"]+common_font["bold"])
        self.layout.addWidget(self.GC_lb_progress_msg, 6, 0, 1, 4)

        self.layout.setSpacing(15)
        self.layout.setRowStretch(7, 1)

        self.GC_lb_result_file.clicked.connect(
            lambda: subprocess.run(['start', 'resource\\chapter.json'], shell=True))

        self.GC_btn_get_chapter.clicked.connect(self.GC_getting)

        self.GC_btn_find.clicked.connect(self.GC_find_f_chapter)

    def GC_find_f_chapter(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select old json chapter",
            "./",
            "Json (*.json)"
        )
        if filename:
            self.GC_tb_file_chapters.setText(filename)
            shutil.copyfile(filename, 'resource/chapter.json')

    def GC_getting(self):

        self.GC_refresh()
        self.GC_thread = QThread()

        link = self.GC_tb_link.text()
        server = "mangasee"
        if self.GC_rb_nettruyen.isChecked():
            server = "nettruyen"

        self.worker = GetChapterLink(link, server)

        self.worker.moveToThread(self.GC_thread)

        self.GC_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.GC_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.GC_thread.finished.connect(self.GC_thread.deleteLater)
        self.worker.progress.connect(self.GC_update_progress)

        self.GC_thread.start()

        self.worker.finished.connect(self.GC_finish_getting)

    def GC_refresh(self):
        self.GC_lb_result_file.setText("")
        self.GC_lb_result_file.setEnabled(False)
        self.GC_progress_getting.setValue(0)

    def GC_update_progress(self, data):
        ic(data)
        self.GC_lb_progress_msg.setText(data["title"])
        if data["percent"] == -1:
            self.GC_progress_getting.setValue(0)
        else:
            self.GC_progress_getting.setValue(data["percent"])

    def GC_finish_getting(self, data):
        ic(data)
        if data[1] == 200:
            self.GC_lb_result_file.setText("chapter.json")
            self.GC_lb_result_file.setEnabled(True)
            n.show_toast(msg["suc_gc"]["t"], msg["suc_gc"]
                         ["m"], duration=2, threaded=True)
        else:
            self.GC_lb_progress_msg.setText(data[0])
            n.show_toast('Error!!!', 'Please check all the conditions!',
                         duration=2, threaded=True)
