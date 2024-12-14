import json
import os
import argparse
import sys
from colorama import Fore, Style

from controllers.MetadataController import generate_metadata, METADATA_DEBUG
from common.Commons import extract_number
from common.Constants import file_chapters

def main():
    parser = argparse.ArgumentParser(
        description='Create metadata for comic files')
    parser.add_argument('-b', type=str, help='Bookmark file')
    parser.add_argument('-c', type=str, required=True, help='Comic info file')
    parser.add_argument('-o', type=str, required=True, help='Target folder')
    parser.add_argument('-m', action='store_true', help='Multiple folders')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    
    if METADATA_DEBUG:
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'Tasks: CreateMetadata'.center(70) + Style.RESET_ALL)


    try:
        with open(args.c, 'r', encoding='utf8') as f:
            comic_info = json.load(f)

        bookmark = []
        if args.b is not None:
            with open(args.b, 'r', encoding='utf8') as f:
                bookmark = json.load(f)
        
        if args.m:
            folders = os.listdir()
            folders = [f for f in folders if os.path.isdir(f) and args.o in f]
            if len(folders) == 0:
                raise Exception(f'No folder found with name <{args.o}>')
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
            if not os.path.exists(args.o):
                raise Exception(f'Folder <{args.o}> not found')
            generate_metadata(
                series=comic_info["series"],
                writer=comic_info["writer"],
                vol= comic_info["vol"] if "vol" in comic_info else -1,
                table_content=bookmark,
                summary=comic_info["summary"] if "vol" in comic_info else "",
                target_folder=args.o
            )
    except Exception as e:
        if METADATA_DEBUG:
            print(Fore.RED + f'{"Error:":<20}' + Style.RESET_ALL + f'{str(e): >49}')
            print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)

if __name__ == "__main__":
    main()
