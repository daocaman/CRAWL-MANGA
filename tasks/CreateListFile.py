import argparse
import sys

from controllers.ListAndRenameController import get_list_of_files
from common.Constants import LIST_AND_RENAME_DEBUG
from common.Messages import log_start_function, log_parameter, log_error, END_LOG

def main_process(path: str):
    if LIST_AND_RENAME_DEBUG:
        log_start_function("Tasks: CreateListFile", "main_process")
        log_parameter("Target folder", path, 1)
    try:
        get_list_of_files(path)
        LIST_AND_RENAME_DEBUG and print(END_LOG)
    except Exception as e:
        log_error("Tasks: CreateListFile", "main_process", e)
        LIST_AND_RENAME_DEBUG and print(END_LOG)


def main():
    parser = argparse.ArgumentParser(
        description='Create file rename.json')
    parser.add_argument('-o', type=str, required=True, help='Target folder')

    # Show help if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    main_process(args.o)

if __name__ == "__main__":
    main()
