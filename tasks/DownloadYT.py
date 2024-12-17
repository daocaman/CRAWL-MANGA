import argparse
import sys
import json
from colorama import Fore, Style

from controllers.DownloadYoutubeController import get_playlist_videos, download_yt_process, DOWNLOAD_YOUTUBE_DEBUG

def main_process(youtube_link, type, link_type, file_yt, quality, convert):
    
    if DOWNLOAD_YOUTUBE_DEBUG:
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'DownloadYT: main'.center(70) + Style.RESET_ALL)
    
    try:
        if file_yt:
            with open(file_yt, 'r') as file:
                list_videos = json.load(file)
            for video in list_videos:   
                download_yt_process(video)
        else:
            if link_type == 1:
                download_yt_process({"link": youtube_link, "type": type, "quality": quality, "convert": convert})
            elif link_type == 2:
                list_videos = get_playlist_videos(youtube_link)

                list_videos_process = []
                for video in list_videos:
                    list_videos_process.append({"link": video, "type": type, "quality": quality, "convert": convert})
            
                for video in list_videos_process:
                    download_yt_process(video)

        DOWNLOAD_YOUTUBE_DEBUG and print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f'Error: {e}' + Style.RESET_ALL)
        print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)
        return


def main():
    parser = argparse.ArgumentParser(
        description='Download youtube')
    parser.add_argument('-l', type=str, help='Link to the youtube video or playlist')
    parser.add_argument('-t', type=str, help='Type of download')
    parser.add_argument('-l_t', type=int, default=1, help='Youtube link type')
    parser.add_argument('-f_yt', default="", type=str, help='File youtube link')
    parser.add_argument('-q', default="720", type=str, help='Quality of video')
    parser.add_argument('-c', default=False, action='store_true', help='Convert video to mp4')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    
    main_process(args.l, args.t, args.l_t, args.f_yt, args.q, args.c)

if __name__ == "__main__":
    main()

