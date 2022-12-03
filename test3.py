from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import urllib.request

from urllib.request import Request, urlopen
from shutil import copyfileobj

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

links = []
f = open("link.txt", "r")

for x in f:
    print(x)
    links.append(x)


# if you want to use chrome, replace Firefox() with Chrome()
driver = webdriver.Firefox(executable_path=r'./geckodriver.exe')

chapters = open("chapters.txt","w+")

errFile = open("error.txt", "w+")

for idx, i in enumerate(links):
    driver.get(i)  # load the web page

    time.sleep(5)

    imgs = driver.find_elements(By.CLASS_NAME, "bbImage")

    title = driver.title

    title = title.split(" [")[0]

    print(len(imgs))

    chapters.write("Fol: "+title+"\n")

    for idxx, img in enumerate(imgs):
        print(img.get_attribute("src"))
        chapters.write(img.get_attribute("src")+"\n")



    # if not os.path.exists("File "+str(count)):
    #     os.mkdir("File "+str(count))

    # for idxx, img in enumerate(imgs):
    #     print(img.get_attribute("src"))
    #     print(img.get_attribute("title"))

    #     try:
    #         urllib.request.urlretrieve(img.get_attribute(
    #             "src"), "File "+str(count)+"/"+str(idxx)+".jpg")
    #     except:
    #         errFile.write("File "+str(count)+"/"+str(idxx) +
    #                       ".jpg" + " - "+img.get_attribute("src")+"\n")
    #         continue

    # count += 1


chapters.close()

driver.close()
