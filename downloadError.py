import requests
from icecream import ic

links = []
f = open("error.txt", "r", encoding="utf8")

servers = {
    "mangasee": "https://mangasee123.com/",
    "nettruyen": "https://www.nettruyentv.com/",
    "sinhvien": "https://kenhsinhvien.vn/"
}


errFile = open("error - new.txt", "w+", encoding="utf8")
for x in f:
    links.append(x)

for img in links:

    spe = img.split(" - ")

    tmp = ""
    if len(spe) != 2:
        tmp =  spe[0:-1]
        tmp= " - ".join(tmp)
    else:
        tmp = spe[0]
    

    try:
        link = spe[-1].replace("\n", "")
        r =requests.get(link, headers={'User-agent': 'Mozilla/5.0', 'Referer': servers["nettruyen"]})

        ic(tmp)
        with open(tmp, "wb") as fd:
            ic(r.status_code)

            if(r.status_code != 200):
                errFile.write(img)
            else:
                fd.write(r.content)
    except Exception as e:
        ic(e)
        errFile.write(img)
        continue
