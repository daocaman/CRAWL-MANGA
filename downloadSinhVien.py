from selenium import webdriver
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier
from icecream import ic

n = ToastNotifier()

links = []
f = open("link.txt", "r")

for x in f:
    links.append(x)

driver = webdriver.Firefox(executable_path=r'./geckodriver.exe')

imgChapters = open("chapters.txt","w+",encoding="utf8")

try:

    for link in links:
        driver.get(link)  # load the web page

        imgs = driver.find_element(By.XPATH, "//*[@id='top']/div[4]/div/div[2]/div[2]/div/div[1]/div[3]/div")

        imgs = imgs.find_element(By.TAG_NAME, 'article')

        imgs = imgs.find_element(By.XPATH, '//div/div[2]/div/div/div[1]/article/div[1]/div')

        imgs = imgs.find_elements(By.CLASS_NAME, 'bbImageWrapper')

        # handle title
        title = driver.title
        title = title.split(" [Tiếng Việt] ")[0]
 
        imgChapters.write("Fol: "+title+"\n")

        ic(title)

        for img in imgs:
            img = img.find_element(By.TAG_NAME, 'img')
            imgChapters.write(img.get_attribute('src')+"\n")

    n.show_toast("Download Sinh vien Truyen","Complete get img src",duration=2)
    imgChapters.close() 
except:
    n.show_toast("Error progress", "Error", duration=2)
    imgChapters.close() 


driver.close()