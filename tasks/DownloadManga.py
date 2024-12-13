import argparse
import os
from icecream import ic

import sys

from controllers.MangaMangaseeController import get_link_chapter_mangasee, get_list_image_mangasee
from controllers.MangaNettruyenController import get_link_chapter_nettruyen, get_list_image_nettruyen
from common.Commons import generate_filename, download_image

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

    if args.s == 1:
        (server, list_chapters) = get_link_chapter_nettruyen(args.l, args.n, args.s_i)
    else:
        (server, list_chapters, cur_path_name, index_name) = get_link_chapter_mangasee(args.l, args.n, args.s_i)

    for chapter in list_chapters:
        if args.s == 1:
            (chapter_name, list_images) = get_list_image_nettruyen(chapter)
        else:
            (chapter_name, list_images) = get_list_image_mangasee(index_name, chapter)
        ic(chapter_name)
        ic(list_images)
        for idx, img in enumerate(list_images):
            if not os.path.exists(chapter_name):
                os.mkdir(chapter_name)
            code_result = download_image(
                count=0, 
                link=img, 
                server=server, 
                file=os.path.join(chapter_name, generate_filename(idx=idx, ext=".jpg") )
            )
            if code_result != 200:
                ic(f"Error download image {img}")


if __name__ == "__main__":  
    main()