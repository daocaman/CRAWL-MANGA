import argparse
import sys
import json
from colorama import Fore, Style

from controllers.DownloadYoutubeController import get_playlist_videos, download_yt_process, DOWNLOAD_YOUTUBE_DEBUG

def main():
    parser = argparse.ArgumentParser(
        description='Download youtube')
    parser.add_argument('-l', type=str, help='Link to the youtube video or playlist')
    parser.add_argument('-t', type=str, help='Type of download')
    parser.add_argument('-l_t', type=int, default=1, help='Youtube link type')
    parser.add_argument('-f_yt', default="", type=str, help='File youtube link')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    try:
        if DOWNLOAD_YOUTUBE_DEBUG:
            print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
            print(Fore.YELLOW + 'DownloadYT: main'.center(70) + Style.RESET_ALL)
        
        if args.f_yt:
            with open(args.f_yt, 'r') as file:
                list_videos = json.load(file)
            for video in list_videos:
                download_yt_process(video)
        else:
            if args.l_t == 1:
                download_yt_process({"link": args.l, "type": args.t})
            elif args.l_t == 2:
                list_videos = get_playlist_videos(args.l)

                list_videos_process = []
                for video in list_videos:
                    list_videos_process.append({"link": video, "type": args.t})

            
                for video in list_videos_process:
                    download_yt_process(video)

        DOWNLOAD_YOUTUBE_DEBUG and print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f'Error: {e}' + Style.RESET_ALL)
        print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)
        return


if __name__ == "__main__":
    main()

