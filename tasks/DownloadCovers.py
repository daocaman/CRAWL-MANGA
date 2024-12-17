import argparse
import os
from colorama import Fore, Style
import sys
import multiprocessing

from common.Constants import DOWNLOAD_COVERS_DEBUG
from controllers.DownloadImageController import download_image_process
from controllers.DownloadCoverController import download_cover_process

def main_process(manga_link, number_of_covers):
    if DOWNLOAD_COVERS_DEBUG:
        print(Fore.GREEN + '>' +'='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'Tasks: DownloadCovers'.center(70) + Style.RESET_ALL)
    
    try:

        list_covers = download_cover_process(manga_link)
        
        if len(list_covers) == 0:
            raise Exception('No covers found')

        list_covers = list_covers[:number_of_covers]

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
    

def main():
    parser = argparse.ArgumentParser(
        description='Download covers for a manga')
    parser.add_argument('-l', type=str, required=True, help='Link to the mangadex')
    parser.add_argument('-n', type=int, default=1, help='Number of covers to download')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    main_process(args.l, args.n)

if __name__ == "__main__":  
    main()
