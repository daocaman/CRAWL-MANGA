from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import (QGridLayout, QLabel, QLineEdit, QFileDialog,
                             QProgressBar, QPushButton, QWidget, QSpinBox, QCheckBox)
from QLabelLink import *
from common import *
from SupportFunction import *
import subprocess
import os
import shutil
from assets.Labels import archive_comic_tab


class ArchiveComicTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout()

        self.setLayout(self.layout)

        self.AC_common_str = archive_comic_tab

        self.AC_lb_main_title = QLabel(tabs["AC"]['l'])
        self.AC_lb_main_title.setStyleSheet(generateStyle(
            {**font_bold, **text_success, **font_title}))
        self.layout.addWidget(
            self.AC_lb_main_title, 0, 0, 1, 4, alignment=Qt.AlignCenter)

        self.AC_lb_chapter = QLabel(self.AC_common_str['lb_chapter'])
        self.AC_lb_chapter.setStyleSheet(
            generateStyle({**font_bold, **text_info}))
        self.layout.addWidget(self.AC_lb_chapter, 1, 0, 1, 1)

        self.AC_lbl_chaps = QLabelLink()
        if os.path.exists('resource/vol_chapter.json'):
            self.AC_lbl_chaps.setText('resource/vol_chapter.json')
        self.layout.addWidget(self.AC_lbl_chaps, 1, 1, 1, 3)

        self.AC_lb_cover = QLabel(self.AC_common_str['lb_cover'])
        self.AC_lb_cover.setStyleSheet(generateStyle({**font_bold, **text_info}))
        self.layout.addWidget(self.AC_lb_cover, 2, 0, 1, 1)

        self.AC_lbl_covs = QLabelLink()
        if os.path.exists('resource/covers'):
            self.AC_lbl_covs.setText('resource/covers')
        self.layout.addWidget(self.AC_lbl_covs, 2, 1, 1, 2)

        self.AC_chk_FCover = QCheckBox(
            self.AC_common_str['chk_makeFolderCover'])
        self.AC_chk_FCover.setStyleSheet(generateStyle(text_info))
        self.layout.addWidget(self.AC_chk_FCover, 2, 3, 1, 1)

        self.AC_lb_source = QLabel(self.AC_common_str['lb_source'])
        self.AC_lb_source.setStyleSheet(
            generateStyle({**font_bold, **text_info}))
        self.layout.addWidget(self.AC_lb_source, 3, 0, 1, 1)

        self.AC_tb_src_folder = QLineEdit()
        self.layout.addWidget(self.AC_tb_src_folder, 3, 1, 1, 2)

        self.AC_btn_src = QPushButton(self.AC_common_str['btn_src'])
        self.AC_btn_src.setStyleSheet(generateStyle(btn_primary))
        self.layout.addWidget(self.AC_btn_src, 3, 3, 1, 1)

        self.AC_lb_destination = QLabel(self.AC_common_str['lb_destination'])
        self.AC_lb_destination.setStyleSheet(
            generateStyle({**font_bold, **text_info}))
        self.layout.addWidget(self.AC_lb_destination, 4, 0, 1, 1)

        self.AC_tb_dest_folder = QLineEdit()
        self.layout.addWidget(self.AC_tb_dest_folder, 4, 1, 1, 2)

        self.AC_btn_dest = QPushButton(self.AC_common_str['btn_dest'])
        self.AC_btn_dest.setStyleSheet(generateStyle(btn_success))
        self.layout.addWidget(self.AC_btn_dest, 4, 3, 1, 1)

        self.AC_lb_ComicName = QLabel(self.AC_common_str['lb_comic_name'])
        self.AC_lb_ComicName.setStyleSheet(
            generateStyle({**font_bold, **text_info}))
        self.layout.addWidget(self.AC_lb_ComicName, 5, 0, 1, 1)

        self.AC_tb_comic_name = QLineEdit()
        self.layout.addWidget(self.AC_tb_comic_name, 5, 1, 1, 3)

        self.AC_lb_ComicAuthor = QLabel(self.AC_common_str['lb_comic_author'])
        self.AC_lb_ComicAuthor.setStyleSheet(
            generateStyle({**font_bold, **text_info}))
        self.layout.addWidget(self.AC_lb_ComicAuthor, 6, 0, 1, 1)

        self.AC_tb_comic_author = QLineEdit()
        self.layout.addWidget(self.AC_tb_comic_author, 6, 1, 1, 3)

        self.AC_lb_start_vol = QLabel(self.AC_common_str['lb_comic_start_vol'])
        self.AC_lb_start_vol.setStyleSheet(
            generateStyle({**font_bold, **text_info}))
        self.layout.addWidget(self.AC_lb_start_vol, 7, 0, 1, 1)

        self.AC_sp_start_vol = QSpinBox()
        self.AC_sp_start_vol.setValue(1)
        self.AC_sp_start_vol.setMinimum(1)
        self.AC_sp_start_vol.setMaximum(10000)
        self.layout.addWidget(self.AC_sp_start_vol, 7, 1, 1, 1)

        self.AC_lb_end_vol = QLabel(self.AC_common_str['lb_comic_end_vol'])
        self.AC_lb_end_vol.setStyleSheet(
            generateStyle({**font_bold, **text_info}))
        self.layout.addWidget(self.AC_lb_end_vol, 7, 2, 1, 1)

        self.AC_sp_end_vol = QSpinBox()
        self.AC_sp_end_vol.setValue(1)
        self.AC_sp_end_vol.setMinimum(1)
        self.AC_sp_end_vol.setMaximum(10000)
        self.layout.addWidget(self.AC_sp_end_vol, 7, 3, 1, 1)

        self.AC_progress_down = QProgressBar()
        self.AC_progress_down.setValue(0)
        self.layout.addWidget(self.AC_progress_down, 8, 0, 1, 3)

        self.AC_btn_archive = QPushButton(self.AC_common_str['btn_archive'])
        self.AC_btn_archive.setStyleSheet(generateStyle(btn_danger))
        self.layout.addWidget(self.AC_btn_archive, 8, 3, 1, 1)

        self.AC_lb_progress_txt = QLabel()
        self.AC_lb_progress_txt.setStyleSheet(generateStyle({**font_bold, **text_warning}))
        self.layout.addWidget(self.AC_lb_progress_txt, 9, 0, 1, 3)

        self.layout.setSpacing(15)
        self.layout.setRowStretch(10, 1)
        self.AC_loadData()

        self.AC_lbl_chaps.clicked.connect(self.AC_openChaptersFile)
        self.AC_lbl_covs.clicked.connect(self.AC_openCoverFolder)
        self.AC_btn_src.clicked.connect(self.AC_chooseSrc)
        self.AC_btn_dest.clicked.connect(self.AC_chooseDest)
        self.AC_btn_archive.clicked.connect(self.AC_archiveComic)

    def AC_loadData(self):
        txt_data = self.AC_lbl_chaps.text()
        if os.path.exists(txt_data):
            f = open(txt_data, 'r', encoding='utf-8')
            chapter_vols = json.load(f)
            if "comic" in chapter_vols.keys():
                self.AC_tb_comic_name.setText(chapter_vols["comic"])
            if "author" in chapter_vols.keys():
                self.AC_tb_comic_author.setText(chapter_vols["author"])

            if "vols" in chapter_vols.keys() and len(chapter_vols['vols']) != 0:
                self.AC_sp_end_vol.setValue(len(chapter_vols['vols']))

    def AC_chooseSrc(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        dir = QFileDialog.getExistingDirectory(
            self, "Choose folder to getting chapters and info comic")
        if dir:
            self.AC_tb_src_folder.setText(dir)
            if os.path.exists(dir+'/covers'):
                self.AC_lbl_covs.setText(dir+'/covers')
                self.AC_chk_FCover.setChecked(True)

            if os.path.exists(dir+'/vol_chapter.json'):
                self.AC_lbl_chaps.setText(dir+'/vol_chapter.json')
                self.AC_loadData()
            self.AC_tb_dest_folder.setText(dir)

    def AC_chooseDest(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        dir = QFileDialog.getExistingDirectory(
            self, "Choose destination to archive comic")
        if dir:
            self.AC_tb_dest_folder.setText(dir)

    def AC_openChaptersFile(self):
        if shutil.which('code'):
            subprocess.call(['code', self.AC_lbl_chaps.text()], shell=True)
        else:
            subprocess.call(['start', self.AC_lbl_chaps.text()], shell=True)

    def AC_openCoverFolder(self):
        tmplink = self.AC_lbl_covs.text().split('/')
        tmplink = "\\".join(tmplink)
        subprocess.Popen(['explorer', tmplink], shell=True)

    def AC_archiveComic(self):
        f = open(self.AC_lbl_chaps.text(), 'r')
        vol_chapters = json.load(f)
        f.close()

        vol_chapters['comic'] = self.AC_tb_comic_name.text()
        vol_chapters['author'] = self.AC_tb_comic_author.text()
        vol_chapters['start_vol'] = self.AC_sp_start_vol.value()
        vol_chapters['end_vol'] = self.AC_sp_end_vol.value()

        with open(self.AC_lbl_chaps.text(), "w+") as outfile:
            outfile.write(json.dumps(vol_chapters, indent=2))

        self.AC_thread = QThread()

        self.worker = ArchiveComic(self.AC_tb_src_folder.text(), self.AC_tb_dest_folder.text(
        ), self.AC_lbl_chaps.text(), self.AC_lbl_covs.text(), self.AC_chk_FCover.isChecked())

        self.worker.moveToThread(self.AC_thread)

        self.AC_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.AC_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.AC_thread.finished.connect(self.AC_thread.deleteLater)
        self.worker.progress.connect(self.AC_updateProgress)

        self.AC_thread.start()

        self.worker.finished.connect(self.AC_finish_archive)

    def AC_updateProgress(self, data):
        self.AC_lb_progress_txt.setText(data[0])
        self.AC_progress_down.setValue(data[1])

    def AC_finish_archive(self, data):
        if data[1] == 200:
            n.show_toast(msg["suc_ac"]["t"], msg["suc_ac"]
                            ["m"], duration=2, threaded=True)
        else:
            n.show_toast('Error!!!', 'Something bad happend!!!',
                         duration=2, threaded=True)
