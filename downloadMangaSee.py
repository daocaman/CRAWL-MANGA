from selenium import webdriver
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier
from icecream import ic
from bs4 import BeautifulSoup
import re
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True

def generateName(num, l):
    return "0"*(l - len(num))+num


n = ToastNotifier()

links = []
f = open("link.txt", "r")

for x in f:
    links.append(x)

driver = webdriver.Firefox(
    options=options, executable_path=r'./geckodriver.exe')

imgChapters = open("chapters.txt", "w+", encoding="utf8")

keyword = "Hyde-Closer"

try:

    for link in links:
        driver.get(link)  # load the web page

        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, 'html.parser')

        modal_page = soup.find(id="PageModal")
        cols = modal_page.find_all(class_="col-md-2")

        gal = soup.find(class_="ImageGallery")
        img = gal.find_all(src=re.compile(keyword))[0]

        target = img['src']
        
        ic("Number imgs: ", len(cols))

        ic(target)

        title = soup.find('title')
        title = title.text.replace(" Page 1","").strip()
        
        ic(title)

        imgChapters.write("Fol: "+title+"\n")

        [info_target, page] = target.split(keyword+'/')
        img_info = page.split(".")
        [pg, ext] = [page.replace(
            img_info[len(img_info)-1], ""), img_info[len(img_info)-1]]
        [chap, p] = pg.split("-")

        for i in range(1, len(cols)+1):
            img_tmp = info_target+keyword+'/' + \
                chap+"-"+generateName(str(i), 3)+"."+ext
            imgChapters.write(img_tmp+'\n')

    n.show_toast("Download Manga see", "Complete get img src", duration=2)
    imgChapters.close()
except:
    n.show_toast("Error progress", "Error", duration=2)
    imgChapters.close()


driver.close()
