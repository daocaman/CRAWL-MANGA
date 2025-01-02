import argparse
import os
import sys

from common.Commons import extract_number, generate_filename, is_image_file
from common.Constants import prefix_image_file, RENAME_DEBUG
from common.Messages import log_start_function, log_parameter, log_error, END_LOG

def main_process(target_folder, is_sort, start_index):
    """
    Main process for renaming files
    
    :param target_folder: str, target folder
    :param is_sort: bool, is sort files
    :param start_index: int, start index
    """
    
    if RENAME_DEBUG:
        log_start_function("Tasks: RenameFiles", "main_process")
        log_parameter("target_folder", target_folder, 1)
        log_parameter("is_sort", is_sort, 1)
        log_parameter("start_index", start_index, 1)
    
    try:
        files = os.listdir(target_folder)
        files = [f for f in files if is_image_file(f)]
        files = sorted(files, key=lambda x: extract_number(x, is_sort, start_index))

        for i, f in enumerate(files):
            new_name = generate_filename(prefix_image_file, start_index + i, ".jpg")
            os.rename(os.path.join(target_folder, f), os.path.join(target_folder, new_name))

        RENAME_DEBUG and print(END_LOG)

    except Exception as e:
        log_error("Tasks: RenameFiles", "main_process", e)
        RENAME_DEBUG and print(END_LOG)

def main():
    parser = argparse.ArgumentParser(
        description='Rename files')
    parser.add_argument('-o', type=str, required=True, help='target folder')
    parser.add_argument('-s', default=False, action='store_true', help='Sort file')
    parser.add_argument('-s_i', type=int, default=0, help='Start index')

    # Show help if no arguments provided    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    main_process(args.o, args.s, args.s_i)
        
if __name__ == "__main__":
    main()