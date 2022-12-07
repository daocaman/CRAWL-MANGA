from selenium import webdriver
from win10toast import ToastNotifier
from icecream import ic
from bs4 import BeautifulSoup
import re
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True

n = ToastNotifier()

links = []
f = open("link.txt", "r")

for x in f:
    links.append(x)

driver = webdriver.Firefox(
    options=options, executable_path=r'./geckodriver.exe')

imgChapters = open("chapters.txt", "w+", encoding="utf8")

try:

    for link in links:
        driver.get(link)  # load the web page

        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, 'html.parser')

        title = soup.find('title')
        title = title.text.split(" Next Chap ")[0].strip()
        
        ic(title)

        imgChapters.write("Fol: "+title+"\n")

        imgs = soup.find_all("img", src=re.compile('data=net'))

        ic(len(imgs))


        for idxx, img in enumerate(imgs):
            ic('https:'+img['src'])
            imgChapters.write('https:'+img['src']+"\n")

    n.show_toast("Download Net Truyen", "Complete get img src", duration=2)
    imgChapters.close()
except Exception as e:
    ic(e)
    n.show_toast("Error progress", "Error", duration=2)
    imgChapters.close()


driver.close()
