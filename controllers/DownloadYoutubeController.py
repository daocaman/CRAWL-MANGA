import yt_dlp

from common.Constants import DOWNLOAD_YOUTUBE_DEBUG
from common.Constants import ydl_opts_video, ydl_opts_audio, ydl_opts_playlist, ydl_opts_video_format
from common.Messages import log_start_function, log_parameter, log_error, END_LOG
from common.Messages import MSG_ERR_CONTROLLER_DOWNLOAD_YOUTUBE
from common.Validations import check_valid_video_url, check_valid_playlist_url

DEBUG_OBJ = {
    "download_from_youtube": True,
    "get_playlist_videos": True,
}

def download_from_youtube(url: str, type_download: str, quality: str = "720"):
    """
    Download content from YouTube based on the provided URL and type of download.
    :param url: The URL of the YouTube video or playlist to download.
    :param type_download: The type of content to download. Can be either "video" or "audio".
    :return: None
    """

    # Debug print initial
    if DOWNLOAD_YOUTUBE_DEBUG and DEBUG_OBJ["download_from_youtube"]:
        log_start_function("DownloadYoutubeController", "download_from_youtube")
        log_parameter("URL", url, 1)
        log_parameter("Type download", type_download, 1)
        log_parameter("Quality", quality, 1)
      
    try:
        
        check_valid_video_url(url)
        
        if type_download == "video":
            ydl_opts = ydl_opts_video.copy()
            if quality != "720":
                ydl_opts['format'] = ydl_opts_video_format.format(quality)

        elif type_download == "audio":
            ydl_opts = ydl_opts_audio.copy()
            
        if DOWNLOAD_YOUTUBE_DEBUG and DEBUG_OBJ["download_from_youtube"]:
            log_parameter("YDL opts", ydl_opts, 2)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        DOWNLOAD_YOUTUBE_DEBUG and print(END_LOG)
    except Exception as e:
        if DOWNLOAD_YOUTUBE_DEBUG:
            log_error("DownloadYoutubeController", "download_from_youtube", e)
        raise Exception(MSG_ERR_CONTROLLER_DOWNLOAD_YOUTUBE.format("download_from_youtube"))

def get_playlist_videos(playlist_url: str):
    """
    Get the list of videos from a YouTube playlist.
    :param playlist_url: The URL of the YouTube playlist to extract information from.
    :return: A list of URLs of the videos in the playlist.
    """

    # Debug print initial
    if DOWNLOAD_YOUTUBE_DEBUG and DEBUG_OBJ["get_playlist_videos"]:
        log_start_function("DownloadYoutubeController", "get_playlist_videos")
        log_parameter("Playlist URL", playlist_url, 1)
        
    try:
        check_valid_playlist_url(playlist_url)
        
        ydl_opts = ydl_opts_playlist

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(playlist_url, download=False)
            list_videos = []
            
            if 'entries' in result:
                list_videos = [entry['url'] for entry in result['entries']]
        
            if DOWNLOAD_YOUTUBE_DEBUG and DEBUG_OBJ["get_playlist_videos"]:
                log_parameter("List videos", list_videos, 2)
                print(END_LOG)
            
            return list_videos
    except Exception as e:
        if DOWNLOAD_YOUTUBE_DEBUG:
            log_error("DownloadYoutubeController", "get_playlist_videos", e)
        raise Exception(MSG_ERR_CONTROLLER_DOWNLOAD_YOUTUBE.format("get_playlist_videos"))

def download_yt_process(link_yt_obj):
    """
    Download youtube video process
    :param link_yt_obj: object containing the link, type, and quality
    :return: None
    """
    download_from_youtube(link_yt_obj["link"], link_yt_obj["type"], link_yt_obj["quality"])
