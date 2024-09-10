import argparse
import os
from icecream import ic

import sys

# add the path to the common folder
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..\\common')))
from Commons import get_link_chapter_nettruyen, get_list_image_nettruyen, download_image, generate_filename
from Commons import get_link_chapter_mangasee, get_list_image_mangasee

def main():
    parser = argparse.ArgumentParser(
        description='Download manga')
    parser.add_argument('-l', type=str, required=True, help='Link to the manga page')
    parser.add_argument('-n', type=int, default=-1, required=True, help='Number of chapters to download')
    parser.add_argument('-s', type=int, default=1, required=True, help='Server to download from')

    args = parser.parse_args()

    if args.s == 1:
        (server, list_chapters) = get_link_chapter_nettruyen(args.l, args.n)
    else:
        (server, list_chapters, cur_path_name, index_name) = get_link_chapter_mangasee(args.l, args.n)

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