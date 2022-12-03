import os
import requests
from win10toast import ToastNotifier
from icecream import ic

n = ToastNotifier()

f = open("chapters.txt", "r", encoding="utf8")

crrFolder = ""

count = 0

errFile = open("error.txt", "w+", encoding="utf8")

countChapter = 0

countFolder = 0

servers = {
    "mangasee": "https://mangasee123.com/",
    "nettruyen": "https://www.nettruyentv.com/",
    "sinhvien": "https://kenhsinhvien.vn/"
}

try:

    for i, x in enumerate(f):

        if "Fol: " in x:
            ic(x)

            countChapter += 1

            folname = x.split("Fol: ")[1].replace("\n", "")
            crrFolder = folname
            count = 0

            countFolder += 1
            if not os.path.exists(folname):
                os.mkdir(crrFolder)

        else:
            try:
                count += 1
                r = requests.get(x.replace("\n", ""), headers={
                                 'User-agent': 'Mozilla/5.0', 'Referer': servers["mangasee"]}, timeout=(3, 5))
                ic(r)

                # two digit for one file image (mod=2)
                mod = 2
                if mod == 2:
                    if count < 10:
                        with open(crrFolder+"/"+"0"+str(count)+".jpg", "wb") as fd:

                            if(r.status_code != 200):
                                errFile.write(
                                    crrFolder+"/"+str(count)+".jpg" + " - "+x+"\n")
                            else:
                                fd.write(r.content)
                    else:
                        with open(crrFolder+"/"+str(count)+".jpg", "wb") as fd:

                            if(r.status_code != 200):
                                errFile.write(
                                    crrFolder+"/"+str(count)+".jpg" + " - "+x+"\n")
                            else:
                                fd.write(r.content)
                else:

                    with open(crrFolder+"/"+str(count)+".jpg", "wb") as fd:

                        if(r.status_code != 200):
                            errFile.write(
                                crrFolder+"/"+str(count)+".jpg" + " - "+x+"\n")
                        else:
                            fd.write(r.content)

            except Exception as e:
                ic(e)
                errFile.write(crrFolder+"/"+str(count)+".jpg" + " - "+x+"\n")
                continue

    n.show_toast("Download img url", "Complete", duration=2)

    errFile.close()
except:
    n.show_toast("Error progress", "Error", duration=2)
    errFile.close()
