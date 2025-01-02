import argparse
import sys

from controllers.DownloadM3U8Controller import download_m3u8, DOWNLOAD_M3U8_DEBUG
from common.Messages import log_start_function, log_parameter, log_error, END_LOG
from common.Validations import check_file_exist

def main_process(file_path: str):
    """
    Main process for downloading m3u8 video
    :param file_path: path to the file containing the m3u8 video information
    """
    
    if DOWNLOAD_M3U8_DEBUG:
        log_start_function("Tasks: DownloadM3U8", "main_process")
        log_parameter("File path", file_path, 1)
        
    try:
        check_file_exist(file_path)
        download_m3u8(file_path)
        DOWNLOAD_M3U8_DEBUG and print(END_LOG)
    except Exception as e:
        log_error("Tasks: DownloadM3U8", "main_process", e)
        DOWNLOAD_M3U8_DEBUG and print(END_LOG)

def main():
    parser = argparse.ArgumentParser(
        description='Download manga')
    parser.add_argument('-f', type=str, required=True, help='M3U8 file path')
    
    # Check if the user has provided the file path
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    main_process(args.f)

if __name__ == "__main__":
    main()