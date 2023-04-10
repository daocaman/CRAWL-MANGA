from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from win10toast import ToastNotifier
from icecream import ic
from bs4 import BeautifulSoup
import requests
import os
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time

n = ToastNotifier()

options = Options()
options.add_argument("--headless")


link = "https://mangadex.org/title/202d0eaf-df73-4368-a360-0abb28c07b01/bokutachi-wa-hanshoku-wo-yameta?tab=art"


driver = webdriver.Firefox(options = options, service=Service(GeckoDriverManager().install()))
driver.get(link)

soup = BeautifulSoup(driver.page_source, 'html.parser')

imgs = soup.find_all('a',  to=True)

ic(len(imgs))

covers = []
for img in imgs:
    if img['href'] not in covers:
        covers.append(img['href'])
        ic(img['href'])

if not os.path.exists('covers'):
    os.mkdir("covers")


for idx, cover in enumerate(covers):
    r = requests.get(cover, headers={
                                 'User-agent': 'Mozilla/5.0', 'Referer': "https://mangadex.org/"}, timeout=(3, 5))
    if idx <=8:
        filename = "0" + str(idx+1)
    else:
        filename = str(idx+1)
    with open("covers"+"/"+filename+".jpg", "wb") as fd:
        if(r.status_code != 200):
            ic("error")
        else:
            fd.write(r.content)

n.show_toast("Download cover complete","Download success",duration=2)

# from selenium.webdriver.firefox.options import Options

driver.close()
