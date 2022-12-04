import sys
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QGridLayout, QWidget,  QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtWidgets import QLabel, QTabWidget, QLineEdit, QTextEdit, QMessageBox,  QPushButton, QProgressBar, QCheckBox
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal

import qtawesome as qta


import ctypes
myappid = 'crawl_img.v2'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


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
        self.mainTitle_style = "color: #5176cf; font-weight: bold; font-size: 16pt;"
        self.title_style = "color: #74ad5c; font-weight: bold; font-size: 10pt;"

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
        self.tab_gc = QWidget()

        self.tabs.addTab(self.tab_rn, "Rename file")
        self.tabs.addTab(self.tab_gc, "Getting chapter")

    def initRnLayout(self):
        self.tab_rn.layout = QGridLayout(self)

        self.RN_lb_main_title = QLabel("Rename file")
        self.RN_lb_main_title.setStyleSheet(
            "color: #198754; font-weight: bold; font-size: 14pt;")
        self.tab_rn.layout.addWidget(
            self.RN_lb_main_title, 0, 1, Qt.AlignCenter)

        self.RN_lb_src_folder = QLabel("Source folder")
        self.tab_rn.layout.addWidget(self.RN_lb_src_folder, 1, 0)

        self.RN_tb_src_folder = QLineEdit()
        self.tab_rn.layout.addWidget(self.RN_tb_src_folder, 1, 1)

        self.RN_btn_get_list = QPushButton("Get list")
        self.RN_btn_get_list.setStyleSheet(
            "color: #fff; background-color: #007bff")
        self.tab_rn.layout.addWidget(self.RN_btn_get_list, 1, 2)

        self.RN_lb_result = QLabel("Result file")
        self.tab_rn.layout.addWidget(self.RN_lb_result, 2, 0)

        self.RN_lb_result_file = QLabel("rn.txt")
        self.RN_lb_result_file.setStyleSheet("color: #007bff; text-decoration: underline")
        self.tab_rn.layout.addWidget(self.RN_lb_result_file, 2, 1)
        

        self.tab_rn.setLayout(self.tab_rn.layout)


def main():
    app = QApplication(sys.argv)
    ex = CrawlManga()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
