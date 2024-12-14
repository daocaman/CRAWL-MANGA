import yt_dlp
from colorama import Fore, Style
from pprint import pprint
from common.Constants import ydl_opts_video, ydl_opts_audio, save_yt_audio, save_yt_video, ydl_opts_playlist, DOWNLOAD_YOUTUBE_DEBUG

DEBUG_OBJ = {
    "download_from_youtube": True,
    "get_playlist_videos": True,
}

def download_from_youtube(url: str, type_download: str):
    """
    Download content from YouTube based on the provided URL and type of download.
    :param url: The URL of the YouTube video or playlist to download.
    :param type_download: The type of content to download. Can be either "video" or "audio".
    :return: None
    """

    # Debug print initial
    if DOWNLOAD_YOUTUBE_DEBUG and DEBUG_OBJ["download_from_youtube"]:
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'DownloadYoutubeController: download_from_youtube'.center(70) + Style.RESET_ALL)
        print(Fore.BLUE + f'{"URL:":<20}' + Style.RESET_ALL + f'{url: >49}')
        print(Fore.BLUE + f'{"Type download:":<20}' + Style.RESET_ALL + f'{type_download: >49}')

    if type_download == "video":
        ydl_opts = ydl_opts_video
        ydl_opts['outtmpl'] = save_yt_video
    elif type_download == "audio":
        ydl_opts = ydl_opts_audio
        ydl_opts['outtmpl'] = save_yt_audio

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)

def get_playlist_videos(playlist_url: str):
    """
    Get the list of videos from a YouTube playlist.
    :param playlist_url: The URL of the YouTube playlist to extract information from.
    :return: A list of URLs of the videos in the playlist.
    """

    # Debug print initial
    if DOWNLOAD_YOUTUBE_DEBUG and DEBUG_OBJ["get_playlist_videos"]:
        print(Fore.GREEN + '>' + '='*68 + '>' + Style.RESET_ALL)
        print(Fore.YELLOW + 'DownloadYoutubeController: get_playlist_videos'.center(70) + Style.RESET_ALL)
        print(Fore.BLUE + f'{"Playlist URL:":<20}' + Style.RESET_ALL + f'{playlist_url: >49}')

    ydl_opts = ydl_opts_playlist

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)
        list_videos = []
        
        if 'entries' in result:
            list_videos = [entry['url'] for entry in result['entries']]
       

        if DOWNLOAD_YOUTUBE_DEBUG and DEBUG_OBJ["get_playlist_videos"]:
            print(Fore.CYAN + f'{"List videos:":<20}' + Style.RESET_ALL)
            pprint(list_videos)
            print(Fore.GREEN + '<' + '='*68 + '<' + Style.RESET_ALL)

        return list_videos

def download_yt_process(link_yt_obj):
    download_from_youtube(link_yt_obj["link"], link_yt_obj["type"])
