from selenium import webdriver
from selenium.webdriver.common.by import By

link = 'https://www.nettruyentv.com/truyen-tranh/truyen-nhan-atula-shura-no-mon-i-69010'

driver = webdriver.Firefox(executable_path=r'./geckodriver.exe') 

driver.get(link)

target = []

# nettruyen
elements =  driver.find_elements(By.CLASS_NAME, 'chapter')

for ele in elements: 
    find_ele = ele.find_element(By.TAG_NAME , 'a')
    if "truyen-nhan-atula-shura-no-mon-i" in find_ele.get_attribute('href'):
        target.insert(0,find_ele.get_attribute('href'))


f = open("link.txt", "w+")
for i in target:
    f.write(i + "\n")

f.close()

driver.close()
f.close()



