from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from icecream import ic
from bs4 import BeautifulSoup
import re

from win10toast import ToastNotifier
n = ToastNotifier()

options = Options()
options.headless = True

link = 'https://www.nettruyenmin.com/truyen-tranh/reborn-nguoi-dao-tao-sat-thu-73870'

driver = webdriver.Firefox(
    options=options, executable_path=r'./geckodriver.exe')

driver.get(link)



target = []

# mode 1 nettruyen
# mode 2 mangasee

mode = 1

if mode == 1:

    keyword = "reborn-nguoi-dao-tao-sat-thu"

    htmlSource = driver.page_source
    soup = BeautifulSoup(htmlSource, 'html.parser')

    links = soup.find_all(id="nt_listchapter")
    links = links[0].find_all(href=re.compile(keyword))
    ic(len(links))

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
        ic('https://mangasee123.com'+link['href'])
        target.insert(0, 'https://mangasee123.com'+link['href'])

f = open("link.txt", "w+")
for i in target:
    f.write(i + "\n")

n.show_toast("Finish getting link chap", "Success", duration=2)

driver.close()
f.close()
