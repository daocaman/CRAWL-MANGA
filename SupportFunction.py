import os
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from bs4 import BeautifulSoup
from icecream import ic
import requests
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re
import docx
from common import *
import json
from requests.exceptions import *


def generateName(num, l):
    result_str = "0"*l + str(num)
    return result_str[-1*l:]


def generateChapterLink(chapter_str):

    index = ""

    idexStr = int(chapter_str[0])

    if (idexStr != 1):
        index = '-index-' + idexStr

    chapter = int(chapter_str[1:-1])

    odd = ""

    odd_str = int(chapter_str[-1])

    if odd_str != 0:
        odd = "." + str(odd_str)

    return "-chapter-" + str(chapter) + odd + index


def generateChapterImg(chapter_str):
    chapter_str = str(chapter_str)
    chapter = chapter_str[1:-1]
    odd = chapter_str[-1]

    if odd == "0":
        return chapter
    else:
        return chapter + "." + odd


def generatePageImg(page):
    result_page = "000" + str(page)
    return result_page[-3:]


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


def writeChapter(chaps, title, content, targetFile=None, file_type='docx'):
    if file_type == 'docx' and targetFile and isinstance(targetFile, docx.document.Document):
        p = targetFile.add_heading(title.text.strip(), level=1)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p = targetFile.add_paragraph(break_chapter_str)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p = targetFile.add_paragraph(content.strip())
        targetFile.add_page_break()
        return targetFile
    elif file_type == 'txt':
        f = open("resource/"+str(chaps)+'.txt', encoding='utf8', mode='w+')
        f.write(title.text.strip()+"\n")
        f.write(content.strip()+'\n')
        f.close()


class DownloadNovel(QObject):
    finished = pyqtSignal(tuple)
    progress = pyqtSignal(tuple)

    def __init__(self, link, start, end, novelName, author, file_name, server, file_type):
        QObject.__init__(self)
        self.link, self.start, self.end, self.novelName, self.author, self.file_name, self.server, self.file_type = link, start, end, novelName, author, file_name, server, file_type

    def run(self):

        if self.file_name == "":
            filename = "resource/"+self.novelName + ' chap' + \
                str(self.start)+'_'+str(self.end)
        else:
            filename = "resource/"+self.file_name.strip()

        if self.file_type == 0:
            document = Document()

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
                    if self.file_type == 0:
                        document = writeChapter(
                            i, title, content_text, document)
                    else:
                        writeChapter(i, title, content_text, file_type='txt')

                    self.progress.emit((title.text.strip(), int(
                        count*100/(self.end-self.start+1))))

                self.finished.emit((filename+'.docx', 200))
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
                self.finished.emit((filename+'.docx', 200))

            elif self.server == servers_novel["trumtruyen"]:

                count = 0
                for i in range(self.start, self.end+1):
                    count += 1
                    r = requests.get(self.link+str(i))

                    QThread.sleep(1)

                    while r.status_code != 200:
                        r = requests.get(self.link+str(i))
                        QThread.sleep(1)

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

                self.finished.emit((filename+'.docx', 200))

            elif self.server == servers_novel["truyenfull"]:
                count = 0
                for i in range(self.start, self.end+1):
                    count += 1
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

                    self.progress.emit((title.text.strip(), int(
                        count*100/(self.end-self.start+1))))

                self.finished.emit((filename+'.docx', 200))

        except HTTPError:
            self.finished.emit(
                ('No internet connection!!! Please connect internet!', 400))
            if self.file_type == 0:
                core_properties = document.core_properties
                core_properties.author = self.author
                core_properties.comments = "Generated by Crawl Manga - An Đào"
                document.save(filename+".docx")

        except ConnectionError:
            self.finished.emit(
                ('No internet connection!!! Please connect internet!', 400))
            if self.file_type == 0:
                core_properties = document.core_properties
                core_properties.author = self.author
                core_properties.comments = "Generated by Crawl Manga - An Đào"
                document.save(filename+".docx")

        except Exception as e:
            self.finished.emit(('Error!!!', -1))
            ic(e)
            if self.file_type == 0:
                core_properties = document.core_properties
                core_properties.author = self.author
                core_properties.comments = "Generated by Crawl Manga - An Đào"
                document.save(filename+".docx")

        if self.file_type == 0:
            core_properties = document.core_properties
            core_properties.author = self.author
            core_properties.comments = "Generated by Crawl Manga - An Đào"
            document.save(filename+".docx")


class GetChapterLink(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(dict)

    def __init__(self, link, server, keyword=""):
        QObject.__init__(self)
        self.link, self.server, self.keyword = link, server, keyword
        ic(self.keyword)

    def run(self):

        r = requests.get(self.link.strip(), headers={
                         'User-agent': 'Mozilla/5.0'})

        link_f = open('resource/link.txt', 'w+', encoding='utf-8')
        chapters_f = open('resource/chapters.txt', 'w+', encoding='utf-8')

        links = []

        self.progress.emit({"title": "Stage 1", "percent": -1})

        if self.server == "nettruyen":

            htmlSource = r.content
            soup = BeautifulSoup(htmlSource, 'html.parser')

            link_chapters = soup.find_all(id="nt_listchapter")
            link_chapters = link_chapters[0].find_all(
                href=re.compile(self.keyword))

            for idx, link in enumerate(link_chapters):
                links.insert(0, link['href'])
                self.progress.emit(
                    {"title": link['href'], "percent": int((idx+1)*100/len(link_chapters))})

            self.progress.emit({"title": "Stage 2", "percent": -1})

            count = 0
            for link in links:

                link_f.write(link.strip()+'\n')
                count += 1

                r = requests.get(link.strip(), headers={
                    'User-agent': 'Mozilla/5.0'})

                htmlSource = r.content

                soup = BeautifulSoup(htmlSource, 'html.parser')

                title = soup.find('title')
                title = title.text.split(" Next Chap ")[0].strip()

                ic(title)

                chapters_f.write("Fol: "+title+"\n")

                imgs = soup.find_all("img", src=re.compile('data=net'))

                for idxx, img in enumerate(imgs):
                    chapters_f.write('https:'+img['src']+"\n")
                self.progress.emit(
                    {"title": title, "percent": int((count)*100/len(links))})

            link_f.close()
            chapters_f.close()

        else:
            r = requests.get(self.link.strip())

            f = open('resource/test.html', mode='w+', encoding='utf-8')
            f.write(r.text)
            f.close()

            chapters = []
            index_name = ""

            f = open('resource/test.html', mode='r+', encoding='utf-8')

            self.progress.emit({"title": "Stage 1", "percent": -1})
            for line in f.readlines():
                if "vm.CurPathName = " in line:
                    cur_path_name = line.replace("vm.CurPathName = ", "")

                if "vm.IndexName = " in line:
                    index_name = line.replace("vm.IndexName = ", "")
                    index_name = index_name.strip()
                    index_name = index_name.replace('"', '').replace(";", "")

                if "vm.CHAPTERS =" in line:
                    chapters = json.loads(line.replace(
                        'vm.CHAPTERS = ', "").replace(";", ""))

            self.progress.emit({"title": "Stage 2", "percent": -1})

            if len(chapters) != 0:
                for chap_idx, chap in enumerate(chapters):

                    link = "https://mangasee123.com/read-online/" + index_name + \
                        generateChapterLink(chap["Chapter"]) + ".html"
                    link_f.write(link+'\n')
                    r = requests.get(link)
                    f_tmp = open('tmp.html', 'w+', encoding='utf-8')
                    f_tmp.write(r.text)
                    f_tmp.close()
                    f_tmp = open('tmp.html', 'r+', encoding='utf-8')

                    cur_path_name = ""
                    for line in f_tmp.readlines():
                        if "vm.CurPathName = " in line:
                            cur_path_name = line.replace(
                                "vm.CurPathName = ", "").strip().replace(";", "").replace('"', "")
                            break

                    chapters_f.write('Fol: Chapter ' +
                                     generateChapterImg(chap["Chapter"])+'\n')

                    self.progress.emit(
                        {"title": chap["Chapter"], "percent": int((chap_idx+1)/len(chapters)*100)})

                    for p_idx in range(1, int(chap["Page"])+1):
                        img_link = "https://{curPathName}/manga/{index_name}/{directory}{img}.png"
                        img_link = img_link.replace(
                            "{curPathName}", cur_path_name)
                        img_link = img_link.replace("{index_name}", index_name)
                        if chap["Directory"] != "":
                            img_link = img_link.replace(
                                "{directory}", chap["Directory"])
                        else:
                            img_link = img_link.replace("{directory}", "")
                        img_link = img_link.replace("{img}", generateChapterImg(
                            chap["Chapter"])+"-"+generatePageImg(p_idx))

                        chapters_f.write(img_link+'\n')

                link_f.close()
                chapters_f.close()

        self.finished.emit()


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
                if ":" in folname:
                    folname = folname.replace(":", "")
                    crrFolder = folname

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

                                if (r.status_code != 200):
                                    errFile.write(
                                        crrFolder+"/"+str(count)+".jpg" + " - "+x+"\n")
                                else:
                                    fd.write(r.content)
                        else:
                            with open(crrFolder+"/"+str(count)+".jpg", "wb") as fd:

                                if (r.status_code != 200):
                                    errFile.write(
                                        crrFolder+"/"+str(count)+".jpg" + " - "+x+"\n")
                                else:
                                    fd.write(r.content)
                    else:

                        with open(crrFolder+"/"+str(count)+".jpg", "wb") as fd:

                            if (r.status_code != 200):
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


class DownloadInfoComic(QObject):
    finished = pyqtSignal(tuple)
    progress = pyqtSignal(tuple)

    def __init__(self, link, isCover):
        QObject.__init__(self)

        self.link = link
        self.isCover = isCover

    def run(self):

        part_link = self.link.split("/")

        if len(part_link) > 1:
            manga_idx = part_link[-2]

        self.progress.emit(('Stage 1: Download volume info', 0))

        offset = 0

        link_volInfo_api = "https://api.mangadex.org/manga/{manga_idx}/feed?includes[]=scanlation_group&includes[]=user&order[volume]=asc&order[chapter]=asc&offset={offset}"

        link_volInfo_api = link_volInfo_api.replace("{manga_idx}", manga_idx)

        total = 0

        vols = dict()

        while True:
            tmp = link_volInfo_api.replace("{offset}", str(offset))
            r = requests.get(tmp)
            data = r.json()
            total = data['total']
            for chap in data["data"]:
                crr_vol = chap["attributes"]["volume"]
                if chap["attributes"]["chapter"] is not None:
                    crr_chap = int(float(chap["attributes"]["chapter"]))
                else:
                    continue

                if crr_vol not in vols.keys():
                    vols[crr_vol] = []
                if crr_chap not in vols[crr_vol]:
                    vols[crr_vol].append(crr_chap)

            offset += 100
            if offset > total:
                break

        results = []
        for idx, key in enumerate(vols.keys()):
            if key is not None:
                self.progress.emit(('Volume '+str(key), int(
                    (idx+1)*100/(len(vols.keys())))))
                if len(vols[key]) > 2:
                    results.append([int(key), vols[key][0], vols[key][-1]])

        print(results)

        if self.isCover:

            self.progress.emit(('Stage 2: Download cover', 0))

            offset = 0
            link_cov_api = "https://api.mangadex.org/cover?order[volume]=asc&manga[]={manga_idx}&limit=100&offset={offset}"

            link_cov_api = link_cov_api.replace("{manga_idx}", manga_idx)

            if not os.path.exists('resource/covers'):
                os.mkdir("resource/covers")

            covers = []
            while True:
                crr_link = link_cov_api.replace("{offset}", str(offset))
                r = requests.get(crr_link)
                result = r.json()
                data = result["data"]
                for idx, cover in enumerate(data):
                    cover_link = "https://mangadex.org/covers/"
                    cover_link = cover_link + \
                        cover["relationships"][0]['id']+'/' + \
                        cover["attributes"]["fileName"]

                    tmp_vol = cover["attributes"]["volume"]
                    if len(tmp_vol) == 1:
                        tmp_vol = "0" + tmp_vol
                    filename = tmp_vol + "." + \
                        cover["attributes"]["fileName"].split(".")[-1]

                    ic(cover_link)

                    covers.append({'link':cover_link, 'filename': filename})

                offset += 100
                if result['total'] < offset:
                    break

            for idx, cover in enumerate(covers):
                r = requests.get(cover['link'], headers={
                    'User-agent': 'Mozilla/5.0', 'Referer': "https://mangadex.org/"}, timeout=(3, 5))

                if r.status_code != 200:
                    self.finished.emit(("Something error happen!!!", -1))
                    break
                else:
                    with open("resource/covers"+"/"+cover['filename'], "wb") as fd:
                        if (r.status_code != 200):
                            ic("error")
                        else:
                            fd.write(r.content)
                            self.progress.emit((cover['link'], int(
                                (idx+1)*100/(len(covers)))))

        self.finished.emit((results, 200))
