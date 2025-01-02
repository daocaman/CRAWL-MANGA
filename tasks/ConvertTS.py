import argparse
import sys

from controllers.ConvertTSController import convert_ts_to_mp4, CONVERT_TS_DEBUG
from common.Messages import log_start_function, log_parameter, log_error, END_LOG
from common.Validations import check_and_create_folder

def main_process(folder_path):
    """
    Main process for ConvertTS
    :param folder_path: path to the folder containing the ts files
    """
    if CONVERT_TS_DEBUG:
        log_start_function("Tasks: ConvertTS", "main_process")
        log_parameter("Folder path", folder_path, 1)
    
    try:
        check_and_create_folder(folder_path, True)
        convert_ts_to_mp4(folder_path)
        CONVERT_TS_DEBUG and print(END_LOG)
    except Exception as e:
        log_error("Tasks: ConvertTS", "main_process", e)
        CONVERT_TS_DEBUG and print(END_LOG)

def main():
    parser = argparse.ArgumentParser(
        description='Convert ts files to mp4 files')
    parser.add_argument('-o', type=str, required=True, help='Target folder')

    # Show help if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    
    main_process(args.o)

if __name__ == "__main__":
    main()
