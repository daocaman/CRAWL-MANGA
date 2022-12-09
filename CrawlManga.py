import sys
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QGridLayout, QWidget,  QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtWidgets import QLabel, QTabWidget, QLineEdit, QTextEdit, QMessageBox,  QPushButton, QProgressBar, QCheckBox, QFileDialog
from PyQt5.QtGui import QIcon, QIntValidator
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
    "suc_rn": {"t": "Success", "m": "Rename folder done!!!"}
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

        self.tabs.addTab(self.tab_rn, tabs["RN"])
        self.tabs.addTab(self.tab_dv, tabs["DV"])
        self.tabs.addTab(self.tab_gc, tabs["GC"])

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

        self.RN_btn_edit_file = QPushButton(self.RN_common_str["btn_edit_file"])
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
    
    def initDvLayout(self):
        self.tab_dv.layout = QGridLayout(self)

        self.DV_common_str = {
            "lb_link": "Link: ",
            "lb_result": "Resut file: "
        }

        self.DV_lb_main_title = QLabel(tabs["DV"])
        self.DV_lb_main_title.setStyleSheet(
            common_font["bold"]+common_color["success"]+font["title"])
        self.tab_dv.layout.addWidget(
            self.DV_lb_main_title, 0, 0,1,3, alignment=Qt.AlignCenter)

        self.DV_lb_link = QLabel(self.DV_common_str["lb_link"])
        self.DV_lb_link.setStyleSheet(common_font["bold"]+common_color["info"])
        self.tab_dv.layout.addWidget(self.DV_lb_link, 1, 0)

        self.DV_tb_link = QLineEdit()
        self.tab_dv.layout.addWidget(self.DV_tb_link, 1, 1, 1, 2)

        self.DV_lb_result = QLabel(self.DV_common_str["lb_result"])
        self.DV_lb_result.setStyleSheet(common_font["bold"]+common_color["info"])
        self.tab_dv.layout.addWidget(self.DV_lb_result, 2,0)

        self.tab_dv.setLayout(self.tab_dv.layout)




def main():
    app = QApplication(sys.argv)
    ex = CrawlManga()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
