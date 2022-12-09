from bs4 import BeautifulSoup
from icecream import ic
import requests
from docx import Document

import re

document = Document()

start = 1
end = 908

link_novel = 'https://metruyencv.com/truyen/ta-he-chua-tri-tro-choi/chuong-'

book_name = "Ta hệ chữa trị trò chơi"

try:
    for i in range(start, end+1):
        r = requests.get(link_novel+str(i))

        soup = BeautifulSoup(r.content, 'html.parser')

        title = soup.find(class_="nh-read__title")

        ic(title.text.strip())

        content = soup.find_all(id="js-read__content")[0]

        content_text = content.decode_contents()

        divs = content.find_all("div")
        a_s = content.find_all("a")


        divs.sort(key=len, reverse=True)
        for div in divs:
            if str(div) in content_text:
                content_text = content_text.replace(str(div), "")
        
        for a in a_s:
            if str(a) in content_text:
                content_text = content_text.replace(str(a), "")
        
        content_text = content_text.replace("<br/>","\n")
        content_text = content_text.replace("\n\n","\n")
        
        # ic(content_text)


        document.add_heading(title.text.strip(), level=1)
        document.add_paragraph(content_text.strip())
except Exception as e:
    ic(e)
    document.save(book_name +' chap' +
                  str(start)+'_'+str(end)+'.docx')


document.save(book_name +' chap'+str(start)+'_'+str(end)+'.docx')
