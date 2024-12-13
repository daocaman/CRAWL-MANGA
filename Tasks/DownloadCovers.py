import argparse
import os
import requests
from colorama import Fore, Style
import sys

from common.Commons import download_image,  generate_filename
from common.Constants import api_cover, link_cover, server_mangadex, cover_folder, DOWNLOAD_COVERS_DEBUG

def main():
    parser = argparse.ArgumentParser(
        description='Download covers for a manga')
    parser.add_argument('-l', type=str, required=True, help='Link to the mangadex')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    
    DOWNLOAD_COVERS_DEBUG and print(Fore.GREEN + '='*70 + Style.RESET_ALL)
    DOWNLOAD_COVERS_DEBUG and print(Fore.YELLOW + 'Tasks: DownloadCovers'.center(70) + Style.RESET_ALL)
    
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
                list_covers.append({
                    "vol": tmp_vol,
                    "link": cover_link
                })

            offset += 100
            if result['total'] < offset:
                break
        
        for cover in list_covers:
            code_result = download_image(
                count=0, 
                link=cover["link"], 
                server=server_mangadex, 
                file=os.path.join(cover_folder, generate_filename(idx=cover["vol"], ext=".jpg" ))
            )
            if code_result != 200:
                DOWNLOAD_COVERS_DEBUG and print(Fore.RED + f'{"Error:":<20}' + Style.RESET_ALL + f'Download this cover {cover["link"]} failed')
    except Exception as e:
        DOWNLOAD_COVERS_DEBUG and print(Fore.RED + f'{"Error:":<20}' + Style.RESET_ALL + f'{str(e): >49}')
        DOWNLOAD_COVERS_DEBUG and print(Fore.GREEN + '='*70 + Style.RESET_ALL)

if __name__ == "__main__":  
    main()
