from PyQt5.QtCore import Qt, QThread

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QGridLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QWidget, QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView)
from QLabelLink import *
from common import *
from SupportFunction import *
import subprocess


class DownloadInfoComicTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout()

        self.setLayout(self.layout)

        self.GI_common_str = {
            'lb_link': "Link Mangadex: ",
            "chkb_cover": "Download cover",
            "chkb_vol_chapters": "Download volume chapters",
            'lb_info': "Comic volume info",
            'lb_progress': "Progress: ",
            'lb_cover': 'Cover: ',
            'lb_chap_info': "Volume chapter info: ",
            'btn_download': 'Download',
            'btn_save_info': 'Save info'
        }

        self.GI_lb_main_title = QLabel(tabs["GI"]['l'])
        self.GI_lb_main_title.setStyleSheet(
            common_font["bold"]+common_color["success"]+font["title"])
        self.layout.addWidget(
            self.GI_lb_main_title, 0, 0, 1, 4, alignment=Qt.AlignCenter)

        self.GI_lb_link = QLabel(self.GI_common_str['lb_link'])
        self.GI_lb_link.setStyleSheet(common_font["bold"]+common_color["info"])
        self.layout.addWidget(self.GI_lb_link, 1, 0, 1, 1)

        self.GI_tb_link = QLineEdit()
        self.layout.addWidget(self.GI_tb_link, 1, 1, 1, 3)

        self.GI_chk_cover = QCheckBox(self.GI_common_str["chkb_cover"])
        self.GI_chk_cover.setStyleSheet(common_color["info"])
        self.layout.addWidget(self.GI_chk_cover, 2, 0, 1, 1)

        self.GI_chk_vol_chapters = QCheckBox(
            self.GI_common_str["chkb_vol_chapters"])
        self.GI_chk_vol_chapters.setStyleSheet(common_color["info"])
        self.GI_chk_vol_chapters.setChecked(True)
        self.layout.addWidget(self.GI_chk_vol_chapters, 2, 1, 1, 1)

        self.GI_progress_down = QProgressBar()
        self.GI_progress_down.setValue(0)
        self.layout.addWidget(self.GI_progress_down, 3, 0, 1, 3)

        self.GI_btn_download = QPushButton(self.GI_common_str["btn_download"])
        self.GI_btn_download.setStyleSheet(btns["default"]+btns["primary"])
        self.layout.addWidget(self.GI_btn_download, 3, 3, 1, 1)

        self.GI_lb_msg = QLabel("")
        self.GI_lb_msg.setStyleSheet(
            common_font["bold"]+common_color["warning"])
        self.layout.addWidget(self.GI_lb_msg, 4, 0, 1,
                              4, alignment=Qt.AlignCenter)

        self.GI_lb_cov = QLabel(self.GI_common_str['lb_cover'])
        self.GI_lb_cov.setStyleSheet(common_font["bold"]+common_color["info"])
        self.layout.addWidget(self.GI_lb_cov, 5, 0, 1, 1)

        self.GI_lbl_cov_res = QLabelLink()
        self.GI_lbl_cov_res.setStyleSheet(
            common_font["bold"]+common_color["info"])
        self.layout.addWidget(self.GI_lbl_cov_res, 5, 1, 1, 3)
        self.GI_lbl_cov_res.setEnabled(False)

        self.GI_lb_info = QLabel(self.GI_common_str['lb_chap_info'])
        self.GI_lb_info.setStyleSheet(common_font["bold"]+common_color["info"])
        self.layout.addWidget(self.GI_lb_info, 6, 0, 1, 1)

        self.GI_lbl_vol_chapters = QLabelLink()
        self.GI_lbl_vol_chapters.setStyleSheet(common_font["bold"]+common_color["info"])
        self.layout.addWidget(self.GI_lbl_vol_chapters, 6, 1, 1, 1)
        self.GI_lbl_vol_chapters.setEnabled(False)

        self.GI_btn_save = QPushButton(self.GI_common_str['btn_save_info'])
        self.GI_btn_save.setStyleSheet(btns["default"]+btns["info"])
        self.layout.addWidget(self.GI_btn_save, 6, 3, 1, 1)

        self.GI_tb_info = QTableWidget()
        self.layout.addWidget(self.GI_tb_info, 7, 0, 3, 4)

        self.layout.setSpacing(15)
        self.layout.setRowStretch(10, 1)

        self.GI_btn_download.clicked.connect(self.GI_downloadInfo)
        self.GI_lbl_cov_res.clicked.connect(self.GI_openCover)
        self.GI_lbl_vol_chapters.clicked.connect(self.GI_openChaptersJSON)
        self.GI_btn_save.clicked.connect(self.GI_saveInfo)

    def GI_openChaptersJSON(self):
        subprocess.run(['start', 'resource\\vol_chapter.json'], shell=True)

    def GI_openCover(self):
        subprocess.Popen(['explorer', 'resource\\covers'])

    def GI_saveInfo(self):

        res_obj = {}

        res_obj["comic"] = self.GI_tb_info.item(0, 1).text()
        res_obj["author"] = self.GI_tb_info.item(1, 1).text()

        res_obj['vols'] = []

        for i in range(2, self.GI_tb_info.rowCount()-1):
            if i != 2:
                if not (int(self.GI_tb_info.item(i, 1).text()) > int(self.GI_tb_info.item(i-1, 2).text())):
                    n.show_toast('Saving error logical', 'Volume ' +
                                 str(i-1), duration=2, threaded=True)
                    return
            tmp_vol = {}
            tmp_vol['Volume'] = int(self.GI_tb_info.item(i, 0).text())
            tmp_vol['start'] = int(self.GI_tb_info.item(i, 1).text())            
            tmp_vol['end'] = int(self.GI_tb_info.item(i, 2).text())
            res_obj['vols'].append(tmp_vol)

        with open("resource/vol_chapter.json", "w+") as outfile:
            outfile.write(json.dumps(res_obj, indent=2))

        self.GI_lbl_vol_chapters.setEnabled(True)
        self.GI_lbl_vol_chapters.setText('vol_chapter.json')

        n.show_toast('Success', 'Saving suceess!!!', duration=2, threaded=True)

    def GI_downloadInfo(self):

        self.link_mangadex = self.GI_tb_link.text().strip()
        if self.link_mangadex == "":
            return

        self.GI_tb_info.setRowCount(0)

        self.GI_thread = QThread()

        self.worker = DownloadInfoComic(
            self.link_mangadex, self.GI_chk_cover.isChecked(), self.GI_chk_vol_chapters.isChecked())

        self.worker.moveToThread(self.GI_thread)

        self.GI_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.GI_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.GI_thread.finished.connect(self.GI_thread.deleteLater)
        self.worker.progress.connect(self.GI_updateProgress)

        self.GI_thread.start()

        self.worker.finished.connect(self.GI_finish_download)

    def GI_updateProgress(self, info):
        self.GI_lb_msg.setText(info[0])
        self.GI_progress_down.setValue(info[1])

    def GI_finish_download(self, info):
        if info[1] == -1:
            n.show_toast('Error', info[0], duration=2, threaded=True)
        elif info[1] == 200:
            if self.GI_chk_cover.isChecked():
                self.GI_lbl_cov_res.setEnabled(True)
                self.GI_lbl_cov_res.setText('resource/covers')

            results_info = info[0]

            self.GI_tb_info.setRowCount(len(results_info)+1)
            self.GI_tb_info.setColumnCount(3)
            self.GI_tb_info.setHorizontalHeaderLabels(
                ["Volume", "Start chap", "End chap"])


            tmp_font = QFont()
            tmp_font.setBold(True)

            self.GI_tb_info.setItem(0, 0, QTableWidgetItem('Author'))
            self.GI_tb_info.item(0,0).setFont(tmp_font)
            self.GI_tb_info.setItem(0, 1, QTableWidgetItem(results_info[0][0]))
            self.GI_tb_info.setSpan(0, 1, 1, 2)

            self.GI_tb_info.setItem(1, 0, QTableWidgetItem('Comic'))
            self.GI_tb_info.item(1,0).setFont(tmp_font)
            self.GI_tb_info.setItem(1, 1, QTableWidgetItem(results_info[0][1]))
            self.GI_tb_info.setSpan(1, 1, 1, 2)

            for idx, vol in enumerate(results_info):
                if idx !=0:
                    self.GI_tb_info.setItem(
                        idx + 1, 0, QTableWidgetItem(str(vol[0])))
                    self.GI_tb_info.setItem(
                        idx + 1, 1, QTableWidgetItem(str(vol[1])))
                    self.GI_tb_info.setItem(
                        idx + 1, 2, QTableWidgetItem(str(vol[2])))

            self.GI_tb_info.horizontalHeader().setStretchLastSection(True)
            self.GI_tb_info.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            n.show_toast(msg["suc_gi"]["t"], msg["suc_gi"]
                            ["m"], duration=2, threaded=True)
