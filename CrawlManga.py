import sys
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QGridLayout, QWidget,  QButtonGroup,  QHeaderView, QRadioButton
from PyQt5.QtWidgets import QLabel, QTabWidget, QLineEdit, QSpinBox, QMessageBox,  QPushButton, QProgressBar, QCheckBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal

from win10toast import ToastNotifier

import os
from icecream import ic

import qtawesome as qta

from SupportFunction import *

import ctypes
myappid = 'crawl_img.v2'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

n = ToastNotifier()

common_color = {
    "primiary": "color: #007bff;",
    "success": "color: #28a745;",
    "info": "color: #17a2b8;",
    "warning": "color: #ffc107;",
    "danger": "color: #dc3545;"
}

common_font = {
    "bold": "font-weight: bold;",
    "underline": "text-decoration: underline;"
}

font = {
    "title": "font-size: 10pt;",
    "mini_title": "font-size: 8pt;",
    "main_title": "font-size: 16pt;"
}

tabs = {
    "RN": "Rename Folder",
    "GC": "Getting Chapter",
    "DV": "Download Novel"
}

btns = {
    "default": "border-radius: 6px; min-width: 80px; min-height: 35px;border-color: #007bff; border: 1px solid #007bff;",
    "primary": "color: #fff;background-color: #007bff;border-color: #007bff;",
    "success": "color: #fff;background-color: #28a745;border-color: #28a745;",
    "info": "color: #fff;background-color: #17a2b8;border-color: #17a2b8;",
    "danger": "color: #fff;background-color: #dc3545;border-color: #dc3545;",
    "warning": "color: #fff;background-color: #ffc107;border-color: #ffc107;",
}

msg = {
    "suc_rn": {"t": "Success", "m": "Rename folder done!!!"},
    "suc_dv": {"t": "Complete", "m": "Download novel done!!!"},
    "suc_gc": {"t": "Complete", "m": "Getting chapter complete!!!"}
}


class CrawlManga(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        resolution = QDesktopWidget().screenGeometry()
        self.title = 'My manga tool'
        self.width = 750
        self.height = 450
        self.left = int((resolution.width() / 2) - (self.width / 2))
        self.top = int((resolution.height() / 2) - (self.height / 2))
        self.icon_app = QIcon("resource/manga.png")
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon("resource/manga.png"))
        self.initMainLayout()
        self.setLayout(self.mainLayout)
        self.show()

    def initMainLayout(self):
        self.mainTitle_style = common_color["primiary"] + \
            font["main_title"]+common_font["bold"]

        self.mainLayout = QGridLayout()

        self.initTitleLayout()
        self.initTabs()

        self.mainLayout.addLayout(
            self.title_layout, 0, 0, alignment=Qt.AlignCenter)
        self.mainLayout.addWidget(self.tabs, 1, 0)

    def initTitleLayout(self):

        self.title_layout = QGridLayout()

        app_title = QLabel("Crawl manga")

        app_title.setStyleSheet(self.mainTitle_style)

        self.title_layout.addWidget(app_title, 0, 1, alignment=Qt.AlignCenter)
        self.title_layout.setSpacing(10)

    def initTabs(self):
        self.tabs = QTabWidget()

        self.tab_rn = QWidget()
        self.initRnLayout()
        self.tab_dv = QWidget()
        self.initDvLayout()
        self.tab_gc = QWidget()
        self.initGcLayout()

        self.tabs.addTab(self.tab_rn, tabs["RN"])
        self.tabs.addTab(self.tab_dv, tabs["DV"])
        self.tabs.addTab(self.tab_gc, tabs["GC"])

    # region Rename tab

    def initRnLayout(self):

        self.tab_rn.layout = QGridLayout(self)

        self.RN_common_str = {
            "lb_src_folder": "Source folder: ",
            "btn_get_list": "Get list",
            "lb_result": "Result file: ",
            "btn_edit_file": "Edit",
            "btn_rename": "Rename"
        }

        self.RN_lb_main_title = QLabel(tabs["RN"])
        self.RN_lb_main_title.setStyleSheet(
            common_font["bold"]+common_color["success"]+font["title"])
        self.tab_rn.layout.addWidget(
            self.RN_lb_main_title, 0, 1, alignment=Qt.AlignCenter)

        self.RN_lb_src_folder = QLabel(self.RN_common_str["lb_src_folder"])
        self.RN_lb_src_folder.setStyleSheet(
            common_font["bold"]+common_color["info"]+font["mini_title"])
        self.tab_rn.layout.addWidget(self.RN_lb_src_folder, 1, 0)

        self.RN_tb_src_folder = QLineEdit()
        self.tab_rn.layout.addWidget(self.RN_tb_src_folder, 1, 1)

        self.RN_btn_get_list = QPushButton(self.RN_common_str["btn_get_list"])
        self.RN_btn_get_list.setStyleSheet(btns["default"]+btns["primary"])
        self.tab_rn.layout.addWidget(self.RN_btn_get_list, 1, 2)

        self.RN_lb_result = QLabel(self.RN_common_str["lb_result"])
        self.RN_lb_result.setStyleSheet(
            common_font["bold"]+common_color["info"]+font["mini_title"])
        self.tab_rn.layout.addWidget(self.RN_lb_result, 2, 0)

        self.RN_lb_result_file = QLabel("")

        self.RN_lb_result_file.setStyleSheet(
            common_font["underline"]+common_color["primiary"])
        self.tab_rn.layout.addWidget(self.RN_lb_result_file, 2, 1)

        self.RN_btn_edit_file = QPushButton(
            self.RN_common_str["btn_edit_file"])
        self.RN_btn_edit_file.setStyleSheet(btns["default"])
        self.tab_rn.layout.addWidget(self.RN_btn_edit_file, 2, 2)

        self.RN_progress_rename = QProgressBar()
        self.RN_progress_rename.setValue(0)
        self.tab_rn.layout.addWidget(self.RN_progress_rename, 3, 0, 1, 2)

        self.RN_btn_rename = QPushButton(self.RN_common_str["btn_rename"])
        self.RN_btn_rename.setStyleSheet(btns["default"] + btns["success"])
        self.tab_rn.layout.addWidget(self.RN_btn_rename, 3, 2)

        self.tab_rn.layout.setSpacing(15)
        self.tab_rn.layout.setRowStretch(4, 1)

        self.RN_resetState()

        # actions

        self.RN_btn_get_list.clicked.connect(self.RN_chooseFolder)
        self.RN_btn_edit_file.clicked.connect(self.RN_openfile)
        self.RN_btn_rename.clicked.connect(self.RN_rename)

        self.tab_rn.setLayout(self.tab_rn.layout)

    def RN_openfile(self):
        os.system('code ' + 'resource/list_files_new.txt')

    def RN_resetState(self):
        self.RN_lb_result_file.setText("")
        self.RN_btn_edit_file.setEnabled(False)
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
            self.RN_btn_edit_file.setEnabled(True)
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

    # endregion

    # region Download novel
    def initDvLayout(self):

        self.tab_dv.layout = QGridLayout(self)

        self.DV_common_str = {
            "lb_link": "Link: ",
            "lb_novel_name": "Novel name: ",
            "lb_start_chap": "From chap: ",
            "lb_end_chap": "To chap: ",
            "lb_result": "Resut file: ",
            "btn_open_location": "Open",
            "btn_download": "Download"
        }

        self.DV_lb_main_title = QLabel(tabs["DV"])
        self.DV_lb_main_title.setStyleSheet(
            common_font["bold"]+common_color["success"]+font["title"])
        self.tab_dv.layout.addWidget(
            self.DV_lb_main_title, 0, 0, 1, 4, alignment=Qt.AlignCenter)

        self.DV_lb_link = QLabel(self.DV_common_str["lb_link"])
        self.DV_lb_link.setStyleSheet(common_font["bold"]+common_color["info"])
        self.tab_dv.layout.addWidget(self.DV_lb_link, 1, 0)

        self.DV_tb_link = QLineEdit()
        self.tab_dv.layout.addWidget(self.DV_tb_link, 1, 1, 1, 3)

        self.DV_lb_novel_name = QLabel(self.DV_common_str["lb_novel_name"])
        self.DV_lb_novel_name.setStyleSheet(
            common_font["bold"]+common_color["info"])
        self.tab_dv.layout.addWidget(self.DV_lb_novel_name, 2, 0)

        self.DV_tb_novel_name = QLineEdit()
        self.tab_dv.layout.addWidget(self.DV_tb_novel_name, 2, 1, 1, 3)

        self.DV_lb_start_chap = QLabel(self.DV_common_str["lb_start_chap"])
        self.DV_lb_start_chap.setStyleSheet(
            common_font["bold"]+common_color["info"])
        self.tab_dv.layout.addWidget(self.DV_lb_start_chap, 3, 0)

        self.DV_spb_start_chap = QSpinBox()
        self.DV_spb_start_chap.setValue(1)
        self.DV_spb_start_chap.setMinimum(1)
        self.DV_spb_start_chap.setMaximum(10000)
        self.tab_dv.layout.addWidget(self.DV_spb_start_chap, 3, 1)

        self.DV_lb_end_chap = QLabel(self.DV_common_str["lb_end_chap"])
        self.DV_lb_end_chap.setStyleSheet(
            common_font["bold"]+common_color["info"])
        self.tab_dv.layout.addWidget(self.DV_lb_end_chap, 3, 2)

        self.DV_spb_end_chap = QSpinBox()
        self.DV_spb_end_chap.setValue(1)
        self.DV_spb_end_chap.setMinimum(1)
        self.DV_spb_end_chap.setMaximum(10000)
        self.tab_dv.layout.addWidget(self.DV_spb_end_chap, 3, 3)

        self.DV_lb_result = QLabel(self.DV_common_str["lb_result"])
        self.DV_lb_result.setStyleSheet(
            common_font["bold"]+common_color["info"])
        self.tab_dv.layout.addWidget(self.DV_lb_result, 4, 0)

        self.DV_lb_file_name = QLabel("")
        self.DV_lb_file_name.setStyleSheet(
            common_font["underline"]+common_color["primiary"])
        self.tab_dv.layout.addWidget(self.DV_lb_file_name, 4, 1, 1, 2)

        self.DV_btn_open_location = QPushButton(
            self.DV_common_str["btn_open_location"])
        self.DV_btn_open_location.setStyleSheet(btns["default"]+btns["info"])
        self.DV_btn_open_location.setEnabled(False)
        self.tab_dv.layout.addWidget(self.DV_btn_open_location, 4, 3)

        self.DV_progress_down = QProgressBar()
        self.DV_progress_down.setValue(0)
        self.tab_dv.layout.addWidget(self.DV_progress_down, 5, 0, 1, 3)

        self.DV_btn_download = QPushButton(self.DV_common_str["btn_download"])
        self.DV_btn_download.setStyleSheet(btns["default"]+btns["danger"])
        self.DV_btn_download.setEnabled(False)
        self.tab_dv.layout.addWidget(self.DV_btn_download, 5, 3)

        self.tab_dv.layout.setSpacing(15)
        self.tab_dv.layout.setRowStretch(6, 1)

        self.DV_tb_link.textChanged.connect(self.DV_updateState)
        self.DV_tb_novel_name.textChanged.connect(self.DV_updateState)

        self.DV_btn_download.clicked.connect(self.DV_downloadNovel)
        self.DV_btn_open_location.clicked.connect(self.DV_openFolder)

        self.tab_dv.setLayout(self.tab_dv.layout)

    def DV_updateState(self, newStr):
        if "http" in self.DV_tb_link.text() and self.DV_tb_novel_name.text() != "":
            self.DV_btn_download.setEnabled(True)

    def DV_downloadNovel(self):
        self.DV_thread = QThread()
        self.worker = DownloadNovel(self.DV_tb_link.text(), self.DV_spb_start_chap.value(
        ), self.DV_spb_end_chap.value(), self.DV_tb_novel_name.text())

        self.worker.moveToThread(self.DV_thread)

        self.DV_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.DV_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.DV_thread.finished.connect(self.DV_thread.deleteLater)
        self.worker.progress.connect(self.DV_updateProgress)

        self.DV_thread.start()

        self.worker.finished.connect(self.DV_finish_download)

    def DV_openFolder(self):
        # os.system("./resource")
        ic(os.getcwd())
        os.system("start " + "resource")

    def DV_updateProgress(self, percent):
        self.DV_progress_down.setValue(percent)

    def DV_finish_download(self, filename):
        self.DV_btn_open_location.setEnabled(True)
        self.DV_lb_file_name.setText(filename)

        n.show_toast(msg["suc_dv"]["t"], msg["suc_dv"]
                     ["m"], duration=2, threaded=True)

    # endregion

    def initGcLayout(self):
        self.tab_gc.layout = QGridLayout(self)

        self.GC_common_str = {
            "lb_link": "Link: ",
            "rb_nettruyen": "nettruyen",
            "rb_mangasee": "mangasee",
            "lb_server": "Server: "
        }

        self.GC_lb_main_title = QLabel(tabs["GC"])
        self.GC_lb_main_title.setStyleSheet(
            common_font["bold"]+common_color["success"]+font["title"])
        self.tab_gc.layout.addWidget(
            self.GC_lb_main_title, 0, 0, 1, 4, alignment=Qt.AlignCenter)

        self.GC_lb_link = QLabel(self.GC_common_str["lb_link"])
        self.GC_lb_link.setStyleSheet(
            common_font["bold"]+common_color["info"])
        self.tab_gc.layout.addWidget(self.GC_lb_link, 1, 0)

        self.GC_tb_link = QLineEdit()
        self.tab_gc.layout.addWidget(self.GC_tb_link, 1, 1, 1, 3)

        self.GC_rb_nettruyen = QRadioButton(
            text=self.GC_common_str["rb_nettruyen"])
        self.GC_rb_mangasee = QRadioButton(
            text=self.GC_common_str["rb_mangasee"])

        self.GC_bg = QButtonGroup()
        self.GC_bg.addButton(self.GC_rb_nettruyen)
        self.GC_bg.addButton(self.GC_rb_mangasee)

        self.GC_lb_server = QLabel(self.GC_common_str["lb_server"])
        self.GC_lb_server.setStyleSheet(
            common_font["bold"]+common_color["info"])
        self.tab_gc.layout.addWidget(self.GC_lb_server, 2,0)

        

        self.tab_gc.layout.addWidget(self.GC_rb_nettruyen, 2, 1)
        self.tab_gc.layout.addWidget(self.GC_rb_mangasee, 2, 2, 1, 2, alignment=Qt.AlignCenter)

        self.tab_gc.setLayout(self.tab_gc.layout)


def main():
    app = QApplication(sys.argv)
    ex = CrawlManga()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
