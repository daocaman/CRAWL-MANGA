import argparse
import sys
import json

from controllers.DownloadYoutubeController import get_playlist_videos, download_yt_process, DOWNLOAD_YOUTUBE_DEBUG
from common.Messages import log_start_function, log_parameter, log_error, END_LOG
from common.Validations import check_file_exist

def main_process(youtube_link: str, type: str, link_type: int, file_yt: str, quality: str):
    """
    Main process for downloading youtube videos
    :param youtube_link: str, link to the youtube video or playlist
    :param type: str, type of download
    :param link_type: int, type of youtube link
    :param file_yt: str, file youtube link
    :param quality: str, quality of video                                   
    """
    
    if DOWNLOAD_YOUTUBE_DEBUG:
        log_start_function("Tasks: DownloadYT", "main_process")
        log_parameter("youtube_link", youtube_link, 1)
        log_parameter("type", type, 1)
        log_parameter("link_type", link_type, 1)
        log_parameter("file_yt", file_yt, 1)
        log_parameter("quality", quality, 1)
    
    try:
        if file_yt:
            check_file_exist(file_yt)
            with open(file_yt, 'r') as file:
                list_videos = json.load(file)
            for video in list_videos:   
                download_yt_process(video)
        else:
            if link_type == 1:
                download_yt_process({"link": youtube_link, "type": type, "quality": quality})
            elif link_type == 2:
                list_videos = get_playlist_videos(youtube_link)

                list_videos_process = []
                for video in list_videos:
                    list_videos_process.append({"link": video, "type": type, "quality": quality})
            
                for video in list_videos_process:
                    download_yt_process(video)

        DOWNLOAD_YOUTUBE_DEBUG and print(END_LOG)
    except Exception as e:
        log_error("Tasks: DownloadYT", "main_process", e)
        DOWNLOAD_YOUTUBE_DEBUG and print(END_LOG)


def main():
    parser = argparse.ArgumentParser(
        description='Download youtube')
    parser.add_argument('-l', type=str, help='Link to the youtube video or playlist')
    parser.add_argument('-t', type=str, help='Type of download')
    parser.add_argument('-l_t', type=int, default=1, help='Youtube link type')
    parser.add_argument('-f_yt', default="", type=str, help='File youtube link')
    parser.add_argument('-q', default="720", type=str, help='Quality of video')

    # Show help if no arguments provided    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    
    main_process(args.l, args.t, args.l_t, args.f_yt, args.q)

if __name__ == "__main__":
    main()

