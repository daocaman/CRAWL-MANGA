import ctypes
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDesktopWidget,  QGridLayout,
                             QLabel, QTabWidget, QWidget)

from downloadComicURLTab import *
from DownloadNovelTab import *
from GettingChapterTab import *
from DownloadInfoComicTab import *
from ArchiveComicTab import *
from RenameTab import *
from SupportFunction import *

myappid = 'an_dao.crawl_img.2'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class CrawlManga(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        resolution = QDesktopWidget().screenGeometry()
        self.title = 'My manga tool'
        self.width = 850
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
        self.mainTitle_style = generateStyle({**text_primary, **font_main_title, **font_bold})  
        ic(self.mainTitle_style)

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

        self.tab_rn = RenameTab()
        self.tab_dv = DownloadNovelTab()
        self.tab_gc = GettingChapterTab()
        self.tab_dc = DownloadComicURLTab()
        self.tab_gi = DownloadInfoComicTab()
        self.tab_ac = ArchiveComicTab()

        self.tabs.addTab(self.tab_rn, tabs["RN"]["s"])
        self.tabs.addTab(self.tab_dv, tabs["DV"]["s"])
        self.tabs.addTab(self.tab_gc, tabs["GC"]["s"])
        self.tabs.addTab(self.tab_dc, tabs["DC"]["s"])
        self.tabs.addTab(self.tab_gi, tabs["GI"]["s"])
        self.tabs.addTab(self.tab_ac, tabs["AC"]["s"])


def main():
    app = QApplication(sys.argv)
    ex = CrawlManga()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
