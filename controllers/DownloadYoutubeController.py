import yt_dlp
from colorama import Fore, Style
from pprint import pprint
from common.Constants import ydl_opts_video, ydl_opts_audio, save_yt_audio, save_yt_video, ydl_opts_playlist, DOWNLOAD_YOUTUBE_DEBUG
import os
import ffmpeg

DEBUG_OBJ = {
    "download_from_youtube": True,
    "get_playlist_videos": True,
}

def download_from_youtube(url: str, type_download: str, quality: str = "720", convert: bool = False):
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
        print(Fore.BLUE + f'{"Quality:":<20}' + Style.RESET_ALL + f'{quality: >49}')

    if type_download == "video":
        ydl_opts = ydl_opts_video
        ydl_opts['outtmpl'] = save_yt_video
        ydl_opts['format'] = f'bestvideo[height<={quality}]+bestaudio/best'

    elif type_download == "audio":
        ydl_opts = ydl_opts_audio
        ydl_opts['outtmpl'] = save_yt_audio

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=False)
        downloaded_file = ydl.prepare_filename(info_dict)
    
    if type_download == "video" and convert:
        convert_file_ffmpeg("mp4", downloaded_file)
    elif type_download == "audio":
        convert_file_ffmpeg("mp3", downloaded_file)
    
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
    
def convert_file_ffmpeg(target_format: str, downloaded_file: str):

    file_name = os.path.splitext(downloaded_file)[0]
    new_file_name = f"{file_name}.{target_format}"
            
    try:
        if target_format == "mp3":
            ffmpeg.input(downloaded_file).output(new_file_name, format='mp3', audio_bitrate='192k').run()
        elif target_format == "mp4":
            ffmpeg.input(downloaded_file).output(new_file_name, format='mp4', vcodec='libx264', acodec='aac').run()
        os.remove(downloaded_file)  # Remove original file after conversion
    except ffmpeg.Error as e:
        print(Fore.RED + f'Error converting file: {e}' + Style.RESET_ALL)
        return False
            
    return True

def download_yt_process(link_yt_obj):
    download_from_youtube(link_yt_obj["link"], link_yt_obj["type"], link_yt_obj["quality"], link_yt_obj["convert"] )
