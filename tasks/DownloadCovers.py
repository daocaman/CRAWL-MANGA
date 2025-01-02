import argparse
import sys

from controllers.DownloadImageController import download_image_process
from controllers.DownloadCoverController import download_cover_process
from common.Commons import execute_process
from common.Constants import DOWNLOAD_COVERS_DEBUG
from common.Messages import log_start_function, log_parameter, log_error, END_LOG
from common.Messages import MSG_ERR_NO_COVERS_FOUND

def main_process(manga_link: str, number_of_covers: int):
    
    
    if DOWNLOAD_COVERS_DEBUG:
        log_start_function("Tasks: DownloadCovers", "main_process")
        log_parameter("Manga link", manga_link, 1)
        log_parameter("Number of covers", number_of_covers, 1)
    
    try:

        list_covers = download_cover_process(manga_link)
        
        if len(list_covers) == 0:
            raise Exception(MSG_ERR_NO_COVERS_FOUND)

        list_covers = list_covers[:number_of_covers]
        
        execute_process(download_image_process, list_covers)
        
        DOWNLOAD_COVERS_DEBUG and print(END_LOG)
        
    except Exception as e:
        log_error("Tasks: DownloadCovers", "main_process", e)
        DOWNLOAD_COVERS_DEBUG and print(END_LOG)
    

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
