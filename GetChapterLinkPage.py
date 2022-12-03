from selenium import webdriver
from selenium.webdriver.common.by import By

link = 'https://www.nettruyentv.com/truyen-tranh/truyen-nhan-atula-shura-no-mon-i-69010'

driver = webdriver.Firefox(executable_path=r'./geckodriver.exe')

driver.get(link)

target = []

# mode 1 nettruyen
# mode 2 mangasee

mode = 1

if mode == 1:

    keyword = "truyen-nhan-atula-shura-no-mon-i"

    elements = driver.find_elements(By.CLASS_NAME, 'chapter')

    for ele in elements:
        find_ele = ele.find_element(By.TAG_NAME, 'a')
        if keyword in find_ele.get_attribute('href'):
            target.insert(0, find_ele.get_attribute('href'))

    f = open("link.txt", "w+")
    for i in target:
        f.write(i + "\n")
else:
    show_ele = driver.find_element(By.CLASS_NAME, "ShowAllChapters")

    if show_ele:
        show_ele.click()

    elements = driver.find_elements(By.CLASS_NAME, 'ChapterLink')

    for ele in elements:
        target.insert(0, ele.get_attribute('href'))

driver.close()
f.close()
