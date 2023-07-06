from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import (QGridLayout, QLabel, QLineEdit,QFileDialog,
                             QProgressBar, QPushButton, QWidget, QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView)
from QLabelLink import *
from common import *
from SupportFunction import *
import subprocess
import os
import shutil

class ArchiveComicTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout()

        self.setLayout(self.layout)

        self.AC_common_str = {
            'lb_chapter': "Chapters info: ",
            'lb_cover': "Covers folder: ",
            'lb_source': 'Source folder: ',
            'lb_destination': 'Destination folder: ',
            'btn_src': 'Get source',
            'btn_dest': 'Get dest',
            'btn_archive': "Archive"
        }

        self.AC_lb_main_title = QLabel(tabs["AC"]['l'])
        self.AC_lb_main_title.setStyleSheet(
            common_font["bold"]+common_color["success"]+font["title"])
        self.layout.addWidget(
            self.AC_lb_main_title, 0, 0, 1, 4, alignment=Qt.AlignCenter)

        self.AC_lb_chapter = QLabel(self.AC_common_str['lb_chapter'])
        self.AC_lb_chapter.setStyleSheet(
            common_font["bold"]+common_color["info"])
        self.layout.addWidget(self.AC_lb_chapter, 1, 0, 1, 1)

        self.AC_lbl_chaps = QLabelLink()
        if os.path.exists('resource/vol_chapter.json'):
            self.AC_lbl_chaps.setText('resource/vol_chapter.json')
        self.layout.addWidget(self.AC_lbl_chaps, 1, 1, 1, 3)

        self.AC_lb_cover = QLabel(self.AC_common_str['lb_cover'])
        self.AC_lb_cover.setStyleSheet(
            common_font["bold"]+common_color["info"])
        self.layout.addWidget(self.AC_lb_cover, 2, 0, 1, 1)

        self.AC_lbl_covs = QLabelLink()
        if os.path.exists('resource/covers'):
            self.AC_lbl_covs.setText('resource/covers')
        self.layout.addWidget(self.AC_lbl_covs, 2, 1, 1, 3)

        self.AC_lb_source = QLabel(self.AC_common_str['lb_source'])
        self.AC_lb_source.setStyleSheet(
            common_font["bold"]+common_color["info"])
        self.layout.addWidget(self.AC_lb_source, 3, 0, 1, 1)

        self.AC_tb_src_folder = QLineEdit()
        self.layout.addWidget(self.AC_tb_src_folder, 3, 1, 1, 2)

        self.AC_btn_src = QPushButton(self.AC_common_str['btn_src'])
        self.AC_btn_src.setStyleSheet(btns["default"]+btns["primary"])
        self.layout.addWidget(self.AC_btn_src, 3, 3, 1, 1)

        self.AC_lb_destination = QLabel(self.AC_common_str['lb_destination'])
        self.AC_lb_destination.setStyleSheet(
            common_font["bold"]+common_color["info"])
        self.layout.addWidget(self.AC_lb_destination, 4, 0, 1, 1)

        self.AC_tb_dest_folder = QLineEdit()
        self.layout.addWidget(self.AC_tb_dest_folder, 4, 1, 1, 2)

        self.AC_btn_dest = QPushButton(self.AC_common_str['btn_dest'])
        self.AC_btn_dest.setStyleSheet(btns["default"]+btns["success"])
        self.layout.addWidget(self.AC_btn_dest, 4, 3, 1, 1)

        self.GI_progress_down = QProgressBar()
        self.GI_progress_down.setValue(0)
        self.layout.addWidget(self.GI_progress_down, 5, 0, 1, 3)

        self.AC_btn_archive = QPushButton(self.AC_common_str['btn_archive'])
        self.AC_btn_archive.setStyleSheet(btns["default"]+btns["danger"])
        self.layout.addWidget(self.AC_btn_archive, 5, 3, 1, 1)

        self.AC_lb_progress_txt = QLabel()
        self.AC_lb_progress_txt.setStyleSheet(
            common_font["bold"]+common_color["warning"])
        self.layout.addWidget(self.AC_lb_progress_txt, 6, 0, 1, 3)

        self.layout.setSpacing(15)
        self.layout.setRowStretch(7, 1)

        self.AC_lbl_chaps.clicked.connect(self.AC_openChaptersFile)
        self.AC_lbl_covs.clicked.connect(self.AC_openCoverFolder)
        self.AC_btn_src.clicked.connect(self.AC_chooseSrc)
        self.AC_btn_dest.clicked.connect(self.AC_chooseDest)

    def AC_chooseSrc(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        dir = QFileDialog.getExistingDirectory(self, "Choose folder to getting chapters and info comic")
        if dir:
            self.AC_tb_src_folder.setText(dir)
            if os.path.exists(dir+'/covers'):
                self.AC_lbl_covs.setText(dir+'/covers')
            if os.path.exists(dir+'/vol_chapter.json'):
                self.AC_lbl_chaps.setText(dir+'/vol_chapter.json')
            self.AC_tb_dest_folder.setText(dir)
    
    def AC_chooseDest(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        dir = QFileDialog.getExistingDirectory(self, "Choose destination to archive comic")
        if dir:
            self.AC_tb_dest_folder.setText(dir)
    
    def AC_openChaptersFile(self):
        if shutil.which('code'):
            subprocess.call(['code', self.AC_lbl_chaps.text()], shell=True )
        else: 
            subprocess.call(['start', self.AC_lbl_chaps.text()], shell=True )

    def AC_openCoverFolder(self):
        subprocess.Popen(['explorer', self.AC_lbl_covs.text()], shell=True)

