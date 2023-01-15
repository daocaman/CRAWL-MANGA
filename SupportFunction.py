import os
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from bs4 import BeautifulSoup
from icecream import ic
import requests
from docx import Document
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import re
from common import *


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


class DownloadNovel(QObject):
    finished = pyqtSignal(str)
    progress = pyqtSignal(tuple)

    def __init__(self, link, start, end, novelName, server):
        QObject.__init__(self)
        self.link, self.start, self.end, self.novelName, self.server = link, start, end, novelName, server

    def run(self):
        document = Document()

        filename = "resource/"+self.novelName + ' chap' + \
            str(self.start)+'_'+str(self.end)

        try:
            if self.server == servers_novel["metruyencv"]:
                count = 0
                for i in range(self.start, self.end+1):
                    count += 1
                    r = requests.get(self.link+str(i))

                    soup = BeautifulSoup(r.content, 'html.parser')

                    title = soup.find(class_="nh-read__title")

                    ic(title.text.strip())

                    content = soup.find_all(id="js-read__content")[0]

                    content_text = content.decode_contents()
                    content_text = content_text.replace("<br/>", "\n")

                    soup = BeautifulSoup(content_text, 'html.parser')
                    content_text = soup.text

                    if "— QUẢNG CÁO —" in content_text:
                        content_text = content_text.replace(
                            "— QUẢNG CÁO —", "")

                    document.add_heading(title.text.strip(), level=1)
                    document.add_paragraph(content_text.strip())

                    self.progress.emit((title.text.strip(), int(
                        count*100/(self.end-self.start+1))))

                self.finished.emit(self.novelName + ' chap' +
                                   str(self.start)+'_'+str(self.end)+'.docx')
            elif self.server == servers_novel["sstruyen"]:

                count = 0
                for i in range(self.start, self.end+1):
                    count += 1
                    r = requests.get(self.link+str(i))

                    soup = BeautifulSoup(r.content, 'html.parser')

                    title = soup.find_all(
                        class_=re.compile("rv-chapt-title"))[0]
                    ic(title.text.strip())

                    content = soup.find_all(class_=re.compile("container1"))

                    content = str(content[0]).replace("<br/>", "\n")
                    soup = BeautifulSoup(content, 'html.parser')
                    content_text = soup.text.strip()

                    document.add_heading(title.text.strip(), level=1)
                    document.add_paragraph(content_text.strip())

                    self.progress.emit((title.text.strip(), int(
                        count*100/(self.end-self.start+1))))
                self.finished.emit(self.novelName + ' chap' +
                                   str(self.start)+'_'+str(self.end)+'.docx')

            elif self.server == servers_novel["trumtruyen"]:

                count = 0
                for i in range(self.start, self.end+1):
                    count += 1
                    r = requests.get(self.link+str(i))

                    QThread.sleep(1)
                    # ic(r.status_code)
                    # while r.status_code != 200:
                    #     r = requests.get(link_novel+str(i))

                    soup = BeautifulSoup(r.content, 'html.parser')

                    title = soup.find_all(
                        class_=re.compile("chapter-title"))[0]

                    content = soup.find_all(id="chapter-c")

                    content = str(content[0]).replace("<br/>", "\n")
                    soup = BeautifulSoup(content, 'html.parser')
                    content_text = soup.text.strip()

                    document.add_heading(title.text.strip(), level=1)
                    document.add_paragraph(content_text.strip())

                    self.progress.emit((title.text.strip(), int(
                        count*100/(self.end-self.start+1))))

                self.finished.emit(self.novelName + ' chap' +
                                   str(self.start)+'_'+str(self.end)+'.docx')
        except Exception as e:
            ic(e)
            document.save(filename+".docx")

        document.save(filename+".docx")

        # os.system("ebook-convert "+doc_name + " " + azw3_name)


class GetChapterLink(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, link, server, keyword=""):
        QObject.__init__(self)
        self.link, self.server, self.keyword = link, server, keyword
        ic(self.keyword)

    def run(self):
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(
            options=options, executable_path=r'./resource/geckodriver.exe')

        driver.get(self.link)
        target = []
        if self.server == "nettruyen":

            htmlSource = driver.page_source
            soup = BeautifulSoup(htmlSource, 'html.parser')

            links = soup.find_all(id="nt_listchapter")
            links = links[0].find_all(href=re.compile(self.keyword))

            for link in links:
                target.insert(0, link['href'])

        else:
            show_ele = driver.find_element(By.CLASS_NAME, "ShowAllChapters")

            if show_ele:
                show_ele.click()

            htmlSource = driver.page_source

            soup = BeautifulSoup(htmlSource, 'html.parser')

            links = soup.find_all(class_="ChapterLink")

            for link in links:
                target.insert(0, 'https://mangasee123.com'+link['href'])

        f = open("./resource/link.txt", "w+")
        for idx, link in enumerate(target):
            f.write(link + "\n")
            self.progress.emit(int((idx+1)*100/len(target)))
        f.close()
        self.finished.emit()
