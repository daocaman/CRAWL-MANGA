import os
import requests
from common.Commons import generate_filename
from common.Constants import api_cover, link_cover, server_mangadex, cover_folder

def download_cover_process(mangadex_link):
    # get the manga id
    manga_id = mangadex_link.split("/")[-2]

    if not os.path.exists(cover_folder):
        os.mkdir(cover_folder)

    offset = 0
    list_covers = []
    while True:
        current_covers_api = api_cover.format(manga_id, offset)

        r = requests.get(current_covers_api)
        result = r.json()

        data = result["data"]
        for cover in data:
            cover_link = link_cover.format(
                cover["relationships"][0]['id'], cover["attributes"]["fileName"])

            tmp_vol = cover["attributes"]["volume"]
            tmp_locale = cover["attributes"]["locale"]
            tmp_filename = generate_filename(idx=tmp_vol, ext=".jpg")
            list_covers.append({
                "vol": tmp_vol,
                "locale": tmp_locale,
                "link": cover_link,
                "filename": tmp_filename,
                "server": server_mangadex,
                "file": os.path.join(cover_folder, tmp_filename)
            })

        offset += 100
        if result['total'] < offset:
            break
        
    # Filter list covers to remove duplicates, prioritize locale 'ja'
    filtered_covers = {}
    for cover in list_covers:
        vol = cover["vol"]
        locale = cover["locale"]
        if vol not in filtered_covers or locale == 'ja':
            filtered_covers[vol] = cover

    list_covers = list(filtered_covers.values())

    return list_covers
