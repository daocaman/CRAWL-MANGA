from bs4 import BeautifulSoup
from icecream import ic
import requests
from docx import Document
from win10toast import ToastNotifier
n = ToastNotifier()

import re

document = Document()

start = 1
end = 405

link_novel = 'https://sstruyen.vn/ma-thoi-den/chuong-'

book_name = "Ma thổi đèn"


# mode 1 : metruyencv
# mode 2: sstruyen
mode = 2

try:
    if mode == 1:
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
            
            document.add_heading(title.text.strip(), level=1)
            document.add_paragraph(content_text.strip())
    else:

        for i in range(start, end+1):
            r = requests.get(link_novel+str(i))

            soup = BeautifulSoup(r.content, 'html.parser')

            title = soup.find_all(class_=re.compile("rv-chapt-title"))[0]
            ic(title.text.strip())

            content = soup.find_all(class_=re.compile("container1"))

            content = str(content[0]).replace("<br/>","\n")
            soup = BeautifulSoup(content, 'html.parser')
            content_text =soup.text.strip()

            document.add_heading(title.text.strip(), level=1)
            document.add_paragraph(content_text.strip())


except Exception as e:
    ic(e)
    document.save(book_name +' chap' +
                  str(start)+'_'+str(end)+'.docx')


document.save(book_name +' chap'+str(start)+'_'+str(end)+'.docx')
n.show_toast("Complete", "Getting novel complete!!!", duration=2)