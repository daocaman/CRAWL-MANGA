from win10toast import ToastNotifier
from icecream import ic
import requests
import os

n = ToastNotifier()

# change this
link_mangadex = "https://mangadex.org/title/32fdfe9b-6e11-4a13-9e36-dcd8ea77b4e4/kanojo-okarishimasu"

part_link = link_mangadex.split("/")

if len(part_link) > 1:
    manga_idx = part_link[-2]

offset = 0
link_api = "https://api.mangadex.org/cover?order[volume]=asc&manga[]={manga_idx}&limit=100&offset={offset}"

link_api = link_api.replace("{manga_idx}", manga_idx)

r = requests.get(link_api)

data = r.json()

covers = []

if not os.path.exists('covers'):
    os.mkdir("covers")
while True:
    crr_link = link_api.replace("{offset}", str(offset))
    r = requests.get(crr_link)
    result = r.json()
    data = result["data"]
    for cover in data:
        cover_link = "https://mangadex.org/covers/"
        cover_link = cover_link + \
            cover["relationships"][0]['id']+'/' + \
            cover["attributes"]["fileName"]

        tmp_vol = cover["attributes"]["volume"]
        if len(tmp_vol) == 1:
            tmp_vol = "0" + tmp_vol
        filename = tmp_vol + "." + \
            cover["attributes"]["fileName"].split(".")[-1]

        ic(cover_link)
        r = requests.get(cover_link, headers={
                                 'User-agent': 'Mozilla/5.0', 'Referer': "https://mangadex.org/"}, timeout=(3, 5))

        with open("covers"+"/"+filename, "wb") as fd:
            if(r.status_code != 200):
                ic("error")
            else:
                fd.write(r.content)
    
    offset += 100
    if result['total'] < offset:
        break 

n.show_toast('Success','Download cover complete!!!')
