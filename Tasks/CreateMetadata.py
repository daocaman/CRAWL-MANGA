import json
from icecream import ic
import os
import argparse

import sys

# add the path to the common folder
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..\\common')))
from Commons import generate_metadata, extract_number
from Constants import file_chapters


def main():
    parser = argparse.ArgumentParser(
        description='Create metadata for comic files')
    parser.add_argument('-b', type=str, help='bookmark file')
    parser.add_argument('-c', type=str, help='comic info file')
    parser.add_argument('-o', type=str, help='target folder')
    parser.add_argument('-m', action='store_true', help='multiple folders')

    args = parser.parse_args()

    if args.c is None:
        ic("Comic info file is required")
        return

    if args.o is None:
        ic("Target folder is required")
        return

    with open(args.c, 'r', encoding='utf8') as f:
        comic_info = json.load(f)

    bookmark = []
    if args.b is not None:
        with open(args.b, 'r', encoding='utf8') as f:
            bookmark = json.load(f)
    
    if args.m:
        folders = os.listdir()
        folders = [f for f in folders if os.path.isdir(f) and args.o in f]
        folders = sorted(folders, key=lambda x: extract_number(x, True))
        for fol in folders:
            crr_vol = extract_number(fol, True) or -1
            crr_bookmark = []
            if os.path.exists(os.path.join(fol, file_chapters)):
                with open(os.path.join(fol, file_chapters), 'r', encoding='utf8') as f:
                    crr_bookmark = json.load(f)
            generate_metadata(
                series=comic_info["series"],
                writer=comic_info["writer"],
                vol= crr_vol,
                table_content=crr_bookmark,
                target_folder=fol
            )
    else:
        generate_metadata(
            series=comic_info["series"],
            writer=comic_info["writer"],
            vol=comic_info["vol"],
            table_content=bookmark,
            summary=comic_info["summary"],
            target_folder=args.o
        )

if __name__ == "__main__":
    main()
