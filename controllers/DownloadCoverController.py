import os
import requests

from common.Commons import generate_filename
from common.Constants import api_cover, link_cover, server_mangadex, folder_cover, DOWNLOAD_COVERS_DEBUG
from common.Messages import log_start_function, log_parameter,  log_error, END_LOG
from common.Messages import MSG_ERR_CONTROLLER_DOWNLOAD_COVER
from common.Validations import check_and_create_folder

def download_cover_process(mangadex_link: str):
    """
    Process the download manga cover
    :param mangadex_link: mangadex link
    :return: None
    """
    
    if DOWNLOAD_COVERS_DEBUG:
        log_start_function("DownloadCoverController", "download_cover_process")
        log_parameter("mangadex_link", mangadex_link, 1)
    
    try:
        # get the manga id
        manga_id = mangadex_link.split("/")[-2]

        check_and_create_folder(folder_cover, create=True)

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
                    "file": os.path.join(folder_cover, tmp_filename)
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

        if DOWNLOAD_COVERS_DEBUG:
            log_parameter("list_covers", list_covers, 2)
            print(END_LOG)

        return list_covers
    except Exception as e:
        if DOWNLOAD_COVERS_DEBUG:
            log_error("DownloadCoverController", "download_cover_process", e)
        raise Exception(MSG_ERR_CONTROLLER_DOWNLOAD_COVER.format("download_cover_process"))
