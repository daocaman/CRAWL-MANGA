import json
import os
import argparse
import sys

from controllers.MetadataController import generate_metadata, METADATA_DEBUG
from common.Commons import extract_number
from common.Constants import file_chapters
from common.Messages import log_start_function, log_parameter, log_error, END_LOG
from common.Validations import check_file_exist, check_and_get_list_of_folders

def main_process(bookmark_file: str, comic_info_file: str, target_folder: str, is_multiple_folders: bool):
    """
    Main process for CreateMetadata
    :param bookmark_file: path to the bookmark file
    :param comic_info_file: path to the comic info file
    :param target_folder: path to the target folder
    :param is_multiple_folders: flag to indicate if the target folder is a list of folders
    """
    
    if METADATA_DEBUG:
        log_start_function("Tasks: CreateMetadata", "main_process")
        log_parameter("Bookmark file", bookmark_file, 1)
        log_parameter("Comic info file", comic_info_file, 1)
        log_parameter("Target folder", target_folder, 1)
        log_parameter("Is multiple folders", is_multiple_folders, 1)

    try:
        
        check_file_exist(comic_info_file)
        
        with open(comic_info_file, 'r', encoding='utf8') as f:
            comic_info = json.load(f)

        bookmark = []
        if bookmark_file is not None:
            check_file_exist(bookmark_file)
            with open(bookmark_file, 'r', encoding='utf8') as f:
                bookmark = json.load(f)
        
        if is_multiple_folders:
            
            folders = check_and_get_list_of_folders(target_folder)
            
            # Sort folders by volume number
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
                target_folder=target_folder
            )
    except Exception as e:
        log_error("Tasks: CreateMetadata", "main_process", e)
        METADATA_DEBUG and print(END_LOG)


def main():
    parser = argparse.ArgumentParser(
        description='Create metadata for comic files')
    parser.add_argument('-b', type=str, help='Bookmark file')
    parser.add_argument('-c', type=str, required=True, help='Comic info file')
    parser.add_argument('-o', type=str, required=True, help='Target folder')
    parser.add_argument('-m', action='store_true', help='Multiple folders')

    # Show help if no arguments provided    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    
    main_process(args.b, args.c, args.o, args.m)
    
if __name__ == "__main__":
    main()
