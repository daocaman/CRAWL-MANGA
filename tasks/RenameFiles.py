import argparse
import os
import sys
from colorama import Fore, Style

from common.Commons import extract_number, generate_filename, is_image_file
from common.Constants import file_prefix, RENAME_DEBUG

def main_process(target_folder, is_sort, start_index):
    
    if RENAME_DEBUG:
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'Tasks: RenameFiles'.center(70) + Style.RESET_ALL)
    
    try:
        files = os.listdir(target_folder)
        files = [f for f in files if is_image_file(f)]
        files = sorted(files, key=lambda x: extract_number(x, is_sort, start_index))

        for i, f in enumerate(files):
            new_name = generate_filename(file_prefix, start_index + i, ".jpg")
            os.rename(os.path.join(target_folder, f), os.path.join(target_folder, new_name))

        RENAME_DEBUG and print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)

    except Exception as e:
        if RENAME_DEBUG:
            print(Fore.RED + f'Error: {e}' + Style.RESET_ALL)
            print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)

def main():
    parser = argparse.ArgumentParser(
        description='Rename files')
    parser.add_argument('-o', type=str, required=True, help='target folder')
    parser.add_argument('-s', type=bool, default=False, action='store_true', help='Sort file')
    parser.add_argument('-s_i', type=int, default=0, help='Start index')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    main_process(args.o, args.s, args.s_i)
        
if __name__ == "__main__":
    main()