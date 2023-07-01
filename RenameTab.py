import os

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import (QFileDialog, QGridLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QWidget)

from common import *
from SupportFunction import *
from QLabelLink import *
import shutil
import subprocess


class RenameTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout(self)

        self.RN_common_str = {
            "lb_src_folder": "Source folder: ",
            "btn_get_list": "Get list",
            "lb_result": "Result file: ",
            "btn_rename": "Rename"
        }

        self.RN_lb_main_title = QLabel(tabs["RN"]["l"])
        self.RN_lb_main_title.setStyleSheet(
            common_font["bold"]+common_color["success"]+font["title"])
        self.layout.addWidget(
            self.RN_lb_main_title, 0, 1, alignment=Qt.AlignCenter)

        self.RN_lb_src_folder = QLabel(self.RN_common_str["lb_src_folder"])
        self.RN_lb_src_folder.setStyleSheet(
            common_font["bold"]+common_color["info"]+font["mini_title"])
        self.layout.addWidget(self.RN_lb_src_folder, 1, 0)

        self.RN_tb_src_folder = QLineEdit()
        self.layout.addWidget(self.RN_tb_src_folder, 1, 1)

        self.RN_btn_get_list = QPushButton(self.RN_common_str["btn_get_list"])
        self.RN_btn_get_list.setStyleSheet(btns["default"]+btns["primary"])
        self.layout.addWidget(self.RN_btn_get_list, 1, 2)

        self.RN_lb_result = QLabel(self.RN_common_str["lb_result"])
        self.RN_lb_result.setStyleSheet(
            common_font["bold"]+common_color["info"]+font["mini_title"])
        self.layout.addWidget(self.RN_lb_result, 2, 0)

        self.RN_lb_result_file = QLabelLink()
        self.layout.addWidget(self.RN_lb_result_file, 2, 1)

        self.RN_btn_rename = QPushButton(self.RN_common_str["btn_rename"])
        self.RN_btn_rename.setStyleSheet(btns["default"] + btns["success"])
        self.layout.addWidget(self.RN_btn_rename, 2, 2)

        self.RN_progress_rename = QProgressBar()
        self.RN_progress_rename.setValue(0)
        self.layout.addWidget(self.RN_progress_rename, 3, 0, 1, 3)
 
        self.layout.setSpacing(15)
        self.layout.setRowStretch(4, 1)

        self.RN_resetState()

        # actions

        self.RN_btn_get_list.clicked.connect(self.RN_chooseFolder)
        self.RN_lb_result_file.clicked.connect(self.RN_openfile)
        self.RN_btn_rename.clicked.connect(self.RN_rename)

        self.setLayout(self.layout)

    def RN_openfile(self):
        if shutil.which('code'):
            subprocess.call(['code', 'resource\\list_files_new.txt'], shell=True )
        else: 
            subprocess.call(['start', 'resource\\list_files_new.txt'], shell=True )

    def RN_resetState(self):
        self.RN_lb_result_file.setText("")
        self.RN_btn_rename.setEnabled(False)
        self.RN_progress_rename.setValue(0)

    def RN_chooseFolder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        dir = QFileDialog.getExistingDirectory(self, "Choose folder to rename")
        if dir:
            self.RN_tb_src_folder.setText(dir)
            f = open("resource/list_files.txt", encoding="utf8", mode="w+")
            f2 = open("resource/list_files_new.txt",
                      encoding="utf8", mode="w+")
            for file in os.listdir(dir):
                f.write(file+"\n")
                f2.write(file+"\n")
            self.RN_lb_result_file.setText("list_files.txt")
            self.RN_btn_rename.setEnabled(True)
            f.close()
            f2.close()
        else:
            self.RN_resetState()

    def RN_rename(self):
        self.RN_thread = QThread()
        self.worker = RenameFolder(self.RN_tb_src_folder.text())

        self.worker.moveToThread(self.RN_thread)

        self.RN_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.RN_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.RN_thread.finished.connect(self.RN_thread.deleteLater)
        self.worker.progress.connect(self.RN_update_progress)

        self.RN_thread.start()

        self.RN_thread.finished.connect(self.RN_finish_rename)

    def RN_update_progress(self, progress):
        if progress != 1:
            self.RN_files = progress
            self.RN_progress = 0
        else:
            self.RN_progress += 1
            tmp_progress = int(self.RN_progress * 100 / self.RN_files)
            self.RN_progress_rename.setValue(tmp_progress)

    def RN_finish_rename(self):
        n.show_toast(msg["suc_rn"]["t"], msg["suc_rn"]["m"],
                     duration=2, threaded=True)
