from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import pyautogui

import time
import os
import shutil

from win10toast import ToastNotifier

n = ToastNotifier()
# import urllib.request

# from urllib.request import Request, urlopen
# from shutil import copyfileobj

# opener = urllib.request.build_opener()
# opener.addheaders = [('User-agent', 'Mozilla/5.0'),('Referer','http://www.nettruyenvip.com/')]
# urllib.request.install_opener(opener)

links = []
f = open("link.txt", "r")

for x in f:
    print(x)
    links.append(x)

# print(links)

# if you want to use chrome, replace Firefox() with Chrome()
driver = webdriver.Firefox(executable_path=r'./geckodriver.exe')

imgChapters = open("chapters.txt","w+",encoding="utf8")

try:

    for link in links:
        driver.get(link)  # load the web page

        time.sleep(2)

        imgs = driver.find_elements(By.CLASS_NAME, "page-chapter")


        title = driver.title

        title = title.split(" Next Chap ")[0]

        imgChapters.write("Fol: "+title+"\n")

        print(title+"\n")


        for idxx, img in enumerate(imgs):
            targetImg = img.find_element(By.TAG_NAME,"img")

            print(targetImg.get_attribute("src"))
            imgChapters.write(targetImg.get_attribute("src")+"\n")

    n.show_toast("Download Net Truyen","Complete get img src",duration=2)
    imgChapters.close() 
except:
    n.show_toast("Error progress", "Error", duration=2)
    imgChapters.close() 


driver.close()