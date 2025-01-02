import argparse
import os
import sys

from controllers.MangaMangaseeController import get_link_chapter_mangasee, get_list_image_mangasee
from controllers.MangaNettruyenController import get_link_chapter_nettruyen, get_list_image_nettruyen
from controllers.MangaWeebCentralController import get_link_chapter_weebcentral, get_list_image_weebcentral
from controllers.DownloadImageController import download_image_process
from common.Commons import generate_filename, execute_process
from common.Constants import DOWNLOAD_MANGA_DEBUG
from common.Messages import log_start_function, log_parameter, log_error, END_LOG
from common.Validations import check_and_create_folder

def main_process(manga_link: str, number_of_chapters: int, server_type: int, start_index: int):
    """
    Main process for downloading manga
    :param manga_link: link to the manga page
    :param number_of_chapters: number of chapters to download
    :param server_type: server type to download from
    :param start_index: start index
    """
    if DOWNLOAD_MANGA_DEBUG:
        log_start_function("Tasks: DownloadManga", "main_process")
        log_parameter("Manga link", manga_link, 1)
        log_parameter("Number of chapters", number_of_chapters, 1)
        log_parameter("Server type", server_type, 1)
        log_parameter("Start index", start_index, 1)

    try:

        if server_type == 1:
            (server, list_chapters) = get_link_chapter_nettruyen(manga_link, number_of_chapters, start_index)
        elif server_type == 2:
            (server, list_chapters, cur_path_name, index_name) = get_link_chapter_mangasee(manga_link, number_of_chapters, start_index)
        else:
            (server, list_chapters) = get_link_chapter_weebcentral(manga_link, number_of_chapters, start_index )

        if DOWNLOAD_MANGA_DEBUG:
            log_parameter("List chapters", list_chapters, 2)

        for chapter in list_chapters:
            if server_type == 1:
                (chapter_name, list_images) = get_list_image_nettruyen(chapter)
            elif server_type == 2:
                (chapter_name, list_images) = get_list_image_mangasee(index_name, chapter)
            else:
                (chapter_name, list_images) = get_list_image_weebcentral(chapter)

            list_download_img = []

            for idx, img in enumerate(list_images):
                list_download_img.append({
                    "link": img,
                    "server": server,
                    "file": os.path.join(chapter_name, generate_filename(idx=idx, ext=".jpg"))
                })

            check_and_create_folder(chapter_name)
            
            execute_process(download_image_process, list_download_img)

        DOWNLOAD_MANGA_DEBUG and print(END_LOG)
    except Exception as e:
        log_error("Tasks: DownloadManga", "main_process", e)
        DOWNLOAD_MANGA_DEBUG and print(END_LOG)


def main():
    parser = argparse.ArgumentParser(
        description='Download manga')
    parser.add_argument('-l', type=str, required=True, help='Link to the manga page')
    parser.add_argument('-n', type=int, default=-1, required=True, help='Number of chapters to download')
    parser.add_argument('-s', type=int, default=1, required=True, help='Server to download from')
    parser.add_argument('-s_i', type=int, default=-1, required=False, help='Start index')
    
    # Show help if no arguments provided    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    main_process(args.l, args.n, args.s, args.s_i)

if __name__ == "__main__":  
    main()