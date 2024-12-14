import argparse
import os
import requests
from colorama import Fore, Style
import sys
import multiprocessing

from common.Commons import download_image,  generate_filename
from common.Constants import api_cover, link_cover, server_mangadex, cover_folder, DOWNLOAD_COVERS_DEBUG
from controllers.DownloadImageController import download_image_process

def main():
    parser = argparse.ArgumentParser(
        description='Download covers for a manga')
    parser.add_argument('-l', type=str, required=True, help='Link to the mangadex')
    parser.add_argument('-n', type=int, default=1, help='Number of covers to download')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if DOWNLOAD_COVERS_DEBUG:
        print(Fore.GREEN + '>' +'='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'Tasks: DownloadCovers'.center(70) + Style.RESET_ALL)
    
    try:

        # get the manga id
        manga_id = args.l.split("/")[-2]


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

        list_covers = list_covers[:args.n]

        if os.cpu_count() > 1:
            DOWNLOAD_COVERS_DEBUG and print(Fore.CYAN + f'{"Multithreading supported:":<20}' + Style.RESET_ALL + f'{os.cpu_count()}')
            with multiprocessing.Pool(os.cpu_count() // 2) as pool:  
                pool.map(download_image_process, list_covers)
        else:
            for cover in list_covers:
                code_result = download_image_process(cover)

                if code_result != 200:
                    DOWNLOAD_COVERS_DEBUG and print(Fore.RED + f'{"Error:":<20}' + Style.RESET_ALL + f'Download this cover {cover["link"]} failed')
      
    except Exception as e:

        if DOWNLOAD_COVERS_DEBUG:
            print(Fore.RED + f'{"Error:":<20}' + Style.RESET_ALL + f'{str(e): >49}')
            print(Fore.GREEN + '<' +'='*68 + '<' + Style.RESET_ALL)

if __name__ == "__main__":  
    main()
