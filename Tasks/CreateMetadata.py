import json
from icecream import ic
import os
import argparse
import sys

from controllers.MetadataController import generate_metadata
from common.Commons import extract_number
from common.Constants import file_chapters

def main():
    parser = argparse.ArgumentParser(
        description='Create metadata for comic files')
    parser.add_argument('-b', type=str, help='bookmark file')
    parser.add_argument('-c', type=str, required=True, help='comic info file')
    parser.add_argument('-o', type=str, required=True, help='target folder')
    parser.add_argument('-m', action='store_true', help='multiple folders')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

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
        folders = sorted(folders, key=lambda x: extract_number(x, True, False))
        for fol in folders:
            crr_vol = extract_number(fol, True, False) or -1
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
            vol= comic_info["vol"] if "vol" in comic_info else -1,
            table_content=bookmark,
            summary=comic_info["summary"] if "vol" in comic_info else "",
            target_folder=args.o
        )

if __name__ == "__main__":
    main()
