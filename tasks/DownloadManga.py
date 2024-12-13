import argparse
import os
import sys
from colorama import Fore, Style
from pprint import pprint
import concurrent.futures

from controllers.MangaMangaseeController import get_link_chapter_mangasee, get_list_image_mangasee
from controllers.MangaNettruyenController import get_link_chapter_nettruyen, get_list_image_nettruyen
from controllers.DownloadImageController import download_image_process
from common.Commons import generate_filename
from common.Constants import DOWNLOAD_MANGA_DEBUG

def main():
    parser = argparse.ArgumentParser(
        description='Download manga')
    parser.add_argument('-l', type=str, required=True, help='Link to the manga page')
    parser.add_argument('-n', type=int, default=-1, required=True, help='Number of chapters to download')
    parser.add_argument('-s', type=int, default=1, required=True, help='Server to download from')
    parser.add_argument('-s_i', type=int, default=1, required=False, help='Start index')
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    DOWNLOAD_MANGA_DEBUG and print(Fore.GREEN + '>' +'='*68 + '>' + Style.RESET_ALL)
    DOWNLOAD_MANGA_DEBUG and print(Fore.YELLOW + 'DownloadManga: main'.center(70) + Style.RESET_ALL)

    try:

        if args.s == 1:
            (server, list_chapters) = get_link_chapter_nettruyen(args.l, args.n, args.s_i)
        else:
            (server, list_chapters, cur_path_name, index_name) = get_link_chapter_mangasee(args.l, args.n, args.s_i)

        DOWNLOAD_MANGA_DEBUG and print(Fore.CYAN + f'{"List chapters:":<20}' + Style.RESET_ALL)
        DOWNLOAD_MANGA_DEBUG and pprint(list_chapters, indent=2)


        for chapter in list_chapters:
            if args.s == 1:
                (chapter_name, list_images) = get_list_image_nettruyen(chapter)
            else:
                (chapter_name, list_images) = get_list_image_mangasee(index_name, chapter)

            download_img_process = []

            for idx, img in enumerate(list_images):
                download_img_process.append({
                    "link": img,
                    "server": server,
                    "file": os.path.join(chapter_name, generate_filename(idx=idx, ext=".jpg"))
                })

            if not os.path.exists(chapter_name):    
                os.mkdir(chapter_name)

            if os.cpu_count() > 1:
                DOWNLOAD_MANGA_DEBUG and print(Fore.CYAN + f'{"Multithreading supported:":<20}' + Style.RESET_ALL + f'{os.cpu_count()//2}')
                with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() // 2) as executor:
                    executor.map(download_image_process, download_img_process)
            else:
                for idx, img in enumerate(download_img_process):
                    code_result = download_image_process(img)
                    if code_result != 200:
                        DOWNLOAD_MANGA_DEBUG and print(Fore.RED + f'{"Error:":<20}' + Style.RESET_ALL + f'Download this image {img["link"]} failed')

        DOWNLOAD_MANGA_DEBUG and print(Fore.GREEN + '='*70 + Style.RESET_ALL)
    except Exception as e:
        DOWNLOAD_MANGA_DEBUG and print(Fore.RED + f'{"Error:":<20}' + Style.RESET_ALL + f'{str(e): >49}')
        DOWNLOAD_MANGA_DEBUG and print(Fore.GREEN + '<' +'='*68 + '<' + Style.RESET_ALL)

if __name__ == "__main__":  
    main()