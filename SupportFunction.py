import os
from PyQt5.QtCore import  QThread, QObject, pyqtSignal


class RenameFolder(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, link):
        QObject.__init__(self)
        self.link = link
    
    def run(self):

        chapter = []
        f = open("resource/list_files.txt", "r", encoding="utf-8")

        for x in f:
            chapter.append(x)

        chapter_new = []
        f = open("resource/list_files_new.txt", "r", encoding="utf-8")

        for x in f:
            chapter_new.append(x)

        self.progress.emit(len(chapter_new))

        for old, new in zip(chapter, chapter_new):
            os.rename(self.link+"/"+old.replace("\n", ""),
                    self.link+"/"+new.replace("\n", ""))
            self.progress.emit(1)
        
        self.finished.emit()


def rename_folder(link):
    chapter = []
    f = open("resource/list_files.txt", "r", encoding="utf-8")

    for x in f:
        chapter.append(x)

    chapter_new = []
    f = open("resource/list_files_new.txt", "r", encoding="utf-8")

    for x in f:
        chapter_new.append(x)

    for old, new in zip(chapter, chapter_new):
        os.rename(link+"/"+old.replace("\n", ""),
                  link+"/"+new.replace("\n", ""))
