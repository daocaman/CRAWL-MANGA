from selenium import webdriver
from selenium.webdriver.common.by import By

link = 'https://mangasee123.com/manga/Pokmon-Movies-Manga'

driver = webdriver.Firefox(executable_path=r'./geckodriver.exe')

driver.get(link)

show_ele = driver.find_element(By.CLASS_NAME, "ShowAllChapters")

if show_ele:
    show_ele.click()

target = []

# nettruyen
elements = driver.find_elements(By.CLASS_NAME, 'ChapterLink')

for ele in elements:
    target.insert(0, ele.get_attribute('href'))


f = open("link.txt", "w+")
for i in target:
    f.write(i + "\n")

f.close()

driver.close()
f.close()
