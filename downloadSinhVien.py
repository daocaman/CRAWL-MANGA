# from selenium import webdriver
# from selenium.webdriver.common.by import By
from win10toast import ToastNotifier
from icecream import ic
import requests
from bs4 import BeautifulSoup


n = ToastNotifier()

links = []
f = open("link.txt", "r")

for x in f:
    links.append(x)

# driver = webdriver.Firefox(executable_path=r'./geckodriver.exe')

imgChapters = open("chapters.txt","w+",encoding="utf8")

try:

    for link in links:
        r = requests.get(link.strip())

        soup = BeautifulSoup(r.content, 'html.parser')

        title = soup.find('title')
        title = title.text.split(" [Tiếng Việt] ")[0].strip()
        
        ic(title)

        imgChapters.write("Fol: "+title+"\n")

        imgs = soup.find_all("img", class_="bbImage")

        for img in imgs:
            ic(img["src"])
            imgChapters.write(img["src"]+"\n")


    n.show_toast("Download Sinh vien Truyen","Complete get img src",duration=2)
    imgChapters.close() 
except:
    n.show_toast("Error progress", "Error", duration=2)
    imgChapters.close() 

