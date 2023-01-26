import os
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from bs4 import BeautifulSoup
from icecream import ic
import requests
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import re
from common import *


def generateName(num, l):
    return "0"*(l - len(num))+num


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

    def __init__(self, link, start, end, novelName, author, file_name, server):
        QObject.__init__(self)
        self.link, self.start, self.end, self.novelName, self.author, self.file_name, self.server = link, start, end, novelName, author, file_name, server

    def run(self):
        document = Document()
        print(self.server)

        if self.file_name == "":
            filename = "resource/"+self.novelName + ' chap' + \
                str(self.start)+'_'+str(self.end)
        else:
            filename = "resource/"+self.file_name.strip()

        try:
            if self.server == servers_novel["metruyencv"]:
                count = 0
                for i in range(self.start, self.end+1):
                    count += 1
                    r = requests.get(self.link+str(i))

                    soup = BeautifulSoup(r.content, 'html.parser')

                    title = soup.find(class_="nh-read__title")
                    ic(title.text.strip())

                    content = soup.find_all(id="article")[0]

                    content_text = content.decode_contents()
                    content_text = content_text.replace("<br/>", "\n")

                    soup = BeautifulSoup(content_text, 'html.parser')
                    content_text = soup.text


                    if "— QUẢNG CÁO —" in content_text:
                        content_text = content_text.replace(
                            "— QUẢNG CÁO —", "")

                    p = document.add_heading(title.text.strip(), level=1)
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p = document.add_paragraph(break_chapter_str)
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p = document.add_paragraph(content_text.strip())
                    document.add_page_break()

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

                    p = document.add_heading(title.text.strip(), level=1)
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p = document.add_paragraph(break_chapter_str)
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p = document.add_paragraph(content_text.strip())
                    document.add_page_break()

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

                    while r.status_code != 200:
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

                    p = document.add_heading(title.text.strip(), level=1)
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p = document.add_paragraph(break_chapter_str)
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p = document.add_paragraph(content_text.strip())
                    document.add_page_break()

                    self.progress.emit((title.text.strip(), int(
                        count*100/(self.end-self.start+1))))

                self.finished.emit(self.novelName + ' chap' +
                                   str(self.start)+'_'+str(self.end)+'.docx')
            elif self.server == servers_novel["truyenfull"]:
                for i in range(self.start, self.end+1):
                    # r = requests.get(link_novel.replace('{0}', str(i)))
                    r = requests.get(self.link+str(i))

                    soup = BeautifulSoup(r.content, 'html.parser')

                    title = soup.find_all(
                        class_=re.compile("chapter-title"))[0]
                    ic(title.text.strip())

                    content = soup.find_all(id="chapter-c")

                    content = str(content[0]).replace("<br/>", "\n")
                    soup = BeautifulSoup(content, 'html.parser')
                    content_text = soup.text.strip()

                    p = document.add_heading(title.text.strip(), level=1)
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p = document.add_paragraph(break_chapter_str)
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p = document.add_paragraph(content_text.strip())
                    document.add_page_break()
        except Exception as e:
            ic(e)
            core_properties = document.core_properties
            core_properties.author = self.author
            core_properties.comments = "Generated by Crawl Manga - An Đào"
            document.save(filename+".docx")

        core_properties = document.core_properties
        core_properties.author = self.author
        core_properties.comments = "Generated by Crawl Manga - An Đào"
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

            for idx, link in enumerate(links):
                target.insert(0, link['href'])
                self.progress.emit(int((idx+1)*100/len(links)))

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


class GetImageSrc(QObject):
    finished = pyqtSignal(int)
    progress = pyqtSignal(tuple)

    def __init__(self, server, keyword=""):
        QObject.__init__(self)
        self.server, self.keyword = server, keyword

    def run(self):
        if not os.path.exists('resource/link.txt'):
            self.finished.emit(-1)
            return

        if self.server == servers_manga["mangasee"] and self.keyword == "":
            self.finished.emit(401)
            return

        options = Options()
        options.headless = True

        links = []
        f = open("resource/link.txt", "r")

        for x in f:
            links.append(x)

        f.close()

        driver = webdriver.Firefox(
            options=options, executable_path=r'./resource/geckodriver.exe')

        imgChapters = open("./resource/chapters.txt", "w+", encoding="utf8")

        ic(self.server)

        try:
            count = 0
            if self.server == servers_manga["nettruyen"]:
                for link in links:
                    count += 1
                    driver.get(link)  # load the web page

                    htmlSource = driver.page_source
                    soup = BeautifulSoup(htmlSource, 'html.parser')

                    title = soup.find('title')
                    title = title.text.split(" Next Chap ")[0].strip()

                    ic(title)

                    imgChapters.write("Fol: "+title+"\n")

                    imgs = soup.find_all("img", src=re.compile('data=net'))

                    for idxx, img in enumerate(imgs):
                        imgChapters.write('https:'+img['src']+"\n")

                    self.progress.emit((title, int(
                        count*100/(len(links)))))
                imgChapters.close()
                self.finished.emit(200)
            elif self.server == servers_manga["mangasee"]:
                for link in links:
                    count += 1
                    driver.get(link)  # load the web page

                    htmlSource = driver.page_source
                    soup = BeautifulSoup(htmlSource, 'html.parser')

                    modal_page = soup.find(id="PageModal")
                    cols = modal_page.find_all(class_="col-md-2")

                    gal = soup.find(class_="ImageGallery")
                    img = gal.find_all(src=re.compile(self.keyword))[0]

                    target = img['src']

                    title = soup.find('title')
                    title = title.text.replace(" Page 1", "").strip()

                    imgChapters.write("Fol: "+title+"\n")

                    [info_target, page] = target.split(self.keyword+'/')
                    img_info = page.split(".")
                    [pg, ext] = [page.replace(
                        img_info[len(img_info)-1], ""), img_info[len(img_info)-1]]
                    [chap, p] = pg.split("-")

                    for i in range(1, len(cols)+1):
                        img_tmp = info_target+self.keyword+'/' + \
                            chap+"-"+generateName(str(i), 3)+"."+ext
                        imgChapters.write(img_tmp+'\n')

                    self.progress.emit((title, int(
                        count*100/(len(links)))))
                imgChapters.close()
                self.finished.emit(200)
            else:
                for link in links:
                    count += 1
                    r = requests.get(link.strip())

                    soup = BeautifulSoup(r.content, 'html.parser')

                    title = soup.find('title')
                    title = title.text.split(" [Tiếng Việt] ")[0].strip()

                    imgChapters.write("Fol: "+title+"\n")

                    imgs = soup.find_all("img", class_="bbImage")

                    for img in imgs:
                        imgChapters.write(img["src"]+"\n")
                    self.progress.emit((title, int(
                        count*100/(len(links)))))
                imgChapters.close()
                self.finished.emit(200)

        except Exception as e:
            ic(e)
            imgChapters.close()
            self.finished.emit(-1)


class DownloadImage(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(tuple)

    def __init__(self):
        QObject.__init__(self)

    def run(self):

        l_f = open('resource/link.txt', 'r', encoding="utf8")
        server = l_f.readline().strip()

        server = server.replace("https://", "")
        server = "https://"+server.split("/")[0]
        ic(server)

        f = open("resource/chapters.txt", "r", encoding="utf8")

        links = []
        for x in f:
            links.append(x)

        crrFolder = ""

        count = 0
        countAll = 0

        errFile = open("error.txt", "w+", encoding="utf8")

        for i, x in enumerate(links):
            ic(x)
            countAll += 1

            if "Fol: " in x:
                folname = x.split("Fol: ")[1].replace("\n", "")
                crrFolder = folname
                count = 0

                if not os.path.exists(folname):
                    os.mkdir(crrFolder)

                self.progress.emit((folname, int(
                    countAll*100/(len(links)))))

            else:
                try:
                    count += 1
                    r = requests.get(x.replace("\n", ""), headers={
                        'User-agent': 'Mozilla/5.0', 'Referer': server}, timeout=(3, 5))
                    ic(r)

                    # two digit for one file image (mod=2)
                    mod = 2
                    if mod == 2:
                        if count < 10:
                            with open(crrFolder+"/"+"0"+str(count)+".jpg", "wb") as fd:

                                if(r.status_code != 200):
                                    errFile.write(
                                        crrFolder+"/"+str(count)+".jpg" + " - "+x+"\n")
                                else:
                                    fd.write(r.content)
                        else:
                            with open(crrFolder+"/"+str(count)+".jpg", "wb") as fd:

                                if(r.status_code != 200):
                                    errFile.write(
                                        crrFolder+"/"+str(count)+".jpg" + " - "+x+"\n")
                                else:
                                    fd.write(r.content)
                    else:

                        with open(crrFolder+"/"+str(count)+".jpg", "wb") as fd:

                            if(r.status_code != 200):
                                errFile.write(
                                    crrFolder+"/"+str(count)+".jpg" + " - "+x+"\n")
                            else:
                                fd.write(r.content)

                    self.progress.emit(("", int(
                        countAll*100/(len(links)))))
                except Exception as e:
                    ic(e)
                    errFile.write(crrFolder+"/"+str(count) +
                                  ".jpg" + " - "+x+"\n")
                    continue
        self.finished.emit()
        errFile.close()
