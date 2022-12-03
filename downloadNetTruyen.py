from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from win10toast import ToastNotifier
from icecream import ic

n = ToastNotifier()

links = []
f = open("link.txt", "r")

for x in f:
    links.append(x)

driver = webdriver.Firefox(executable_path=r'./geckodriver.exe')

imgChapters = open("chapters.txt", "w+", encoding="utf8")

try:

    for link in links:
        driver.get(link)  # load the web page

        time.sleep(2)

        imgs = driver.find_elements(By.CLASS_NAME, "page-chapter")

        title = driver.title
        title = title.split(" Next Chap ")[0]

        imgChapters.write("Fol: "+title+"\n")

        ic(title)

        for idxx, img in enumerate(imgs):
            targetImg = img.find_element(By.TAG_NAME, "img")
            srcImg = targetImg.get_attribute("src")
            imgChapters.write(srcImg+"\n")

    n.show_toast("Download Net Truyen", "Complete get img src", duration=2)
    imgChapters.close()
except:
    n.show_toast("Error progress", "Error", duration=2)
    imgChapters.close()


driver.close()
