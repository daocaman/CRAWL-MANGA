from selenium import webdriver
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier


def generateName(num, l):
    return "0"*(l - len(num))+num


n = ToastNotifier()

links = []
f = open("link.txt", "r")

for x in f:
    print(x)
    links.append(x)

# print(links)

# if you want to use chrome, replace Firefox() with Chrome()
driver = webdriver.Firefox(executable_path=r'./geckodriver.exe')

imgChapters = open("chapters.txt", "w+", encoding="utf8")

keyword = "Cardcaptor-Sakura-Clear-Card-Arc"

try:

    for link in links:
        driver.get(link)  # load the web page

        modal_page = driver.find_element(By.ID, "PageModal")

        cols = modal_page.find_elements(By.CLASS_NAME, "col-md-2")

        print(len(cols))

        title = driver.title
        print(title+"\n")

        imgChapters.write("Fol: "+title+"\n")

        tmpLink = link.replace("-page-1.html", "")
        gal = driver.find_element(By.CLASS_NAME, "ImageGallery")
        imgs = gal.find_elements(By.TAG_NAME, "img")

        target = ""

        for img in imgs:
            if keyword in img.get_attribute('src'):
                print(img.get_attribute('src'))
                target = img.get_attribute('src')

        [info_target, page] = target.split(keyword+'/')
        img_info = page.split(".")
        [pg, ext] = [page.replace(
            img_info[len(img_info)-1], ""), img_info[len(img_info)-1]]
        print(pg, ext)
        [chap, p] = pg.split("-")

        for i in range(1, len(cols)+1):
            img_tmp = info_target+keyword+'/' + \
                chap+"-"+generateName(str(i), 3)+"."+ext
            print(img_tmp)
            imgChapters.write(img_tmp+'\n')

    n.show_toast("Download Manga see", "Complete get img src", duration=2)
    imgChapters.close()
except:
    n.show_toast("Error progress", "Error", duration=2)

    imgChapters.close()


driver.close()
