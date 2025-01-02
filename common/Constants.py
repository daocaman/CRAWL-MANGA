# Debug variables
COMMON_DEBUG = True

## Manga project debug
DOWNLOAD_MANGA_DEBUG = True
METADATA_DEBUG = True
ARCHIVE_DEBUG = True
DOWNLOAD_COVERS_DEBUG = True
RESIZE_DEBUG = True
REFORMAT_DEBUG = True  
MOVE_CHAP_VOL_DEBUG = True

### Manga server debug
NETTRUYEN_DEBUG = True
MANGASEE_DEBUG = True   
WEEBCENTRAL_DEBUG = True

## Download video project debug
DOWNLOAD_YOUTUBE_DEBUG = True
DOWNLOAD_M3U8_DEBUG = True
CONVERT_TS_DEBUG = True

## Rename project debug
RENAME_DEBUG = True
LIST_AND_RENAME_DEBUG = True

## Download novel project debug
DOWNLOAD_NOVEL_DEBUG = True

# Constants number
max_length_idx = 4
max_download_trial = 3

# Constants string

## server manga
server_nettruyen = "https://nettruyenviet.com"
server_mangasee = "https://mangasee123.com"
server_weebcentral = "https://weebcentral.com"
server_mangadex = "https://mangadex.org"

## api supporting download manga
api_cover = "https://api.mangadex.org/cover?order[volume]=asc&manga[]={0}&limit=100&offset={1}"
link_cover ="https://uploads.mangadex.org/covers/{0}/{1}"
link_yt_video = "https://www.youtube.com/watch?v="
link_yt_playlist = "https://www.youtube.com/playlist?list="
link_chapter_mangasee = "https://mangasee123.com/read-online/{0}.html"
link_chapter_weebcentral = "https://weebcentral.com/series/{0}/full-chapter-list"
## file/folder regex and default file/folder name

### prefix
prefix_image_file = "pages_"
prefix_chapter_folder = "Chapter"

### suffix
suffix_m3u8 = ".m3u8"
suffix_ts = ".ts"
suffix_mp4 = ".mp4"

### regex 
save_yt_audio = "yt_audio/%(title)s.%(ext)s"
save_yt_video = "yt_video/%(title)s.%(ext)s"
manga_vol = "{0} - Vol{1}"

## default file/folder name

### default file name
file_bookmarks = "Bookmarks.json"
file_comic_json = "ComicInfo.json"
file_comic_xml = "ComicInfo.xml"
file_chapters = "Chapters.json"
file_rename_list = "rename_list.json"
file_sample_html = "sample.html"
file_vol_chaps = "vol_chaps.json"
file_yt_json = "youtube.json"
file_m3u8_mp4_json = "m3u8_mp4.json"

### default folder name
folder_running_resource = "running_resource"
folder_sample_resource = "resource"
folder_save_m3u8 = "m3u8"
folder_cover = "Covers"
folder_yt_audio = "yt_audio"
folder_yt_video = "yt_video"
folder_ts = "convert_ts"

# example file content
comic_xml = "<?xml version=\"1.0\" encoding=\"utf-8\"?>" +\
    "\n<ComicInfo xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n" +\
    "{content}" +\
    "\n</ComicInfo>"

comic_series = "\t<Series>{0}</Series>"
comic_writer = "\t<Writer>{0}</Writer>"
comic_volume = "\t<Volume>{0}</Volume>"
comic_summary = "\t<Summary>{0}</Summary>"
comic_page = "\t\t<Page Image=\"{0}\" Bookmark=\"{1}\"/>"
comic_pages_op = "\t<Pages>"
comic_pages_cl = "\t</Pages>"

# example objects

images_ext = [".jpg", ".jpeg", ".png"]

bookmark_obj = {
    "title": "",
    "page": 0,
}

header_obj = {
    'User-agent': 'Mozilla/5.0', 
    'Referer': ""
}

timeout_obj = (3, 5)

horizontal_size = (1448, 1072)
verticle_size = (1072, 1448)


ydl_opts_video_format = 'bestvideo[height<={0}]+bestaudio/best'

ydl_opts_video = {
    'format': ydl_opts_video_format.format(720),  # Download the best quality video and audio with resolution 720 or less
    'outtmpl': save_yt_video,  # Output filename format (video and audio will have the same title)
}

ydl_opts_audio = {
    'format': 'bestaudio/best',  # Download the best quality audio
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',  # Correct key for extracting audio
            'preferredcodec': 'mp3',  # Convert audio to mp3 format
            'preferredquality': '192',  # Set the preferred quality to 192 kbps
        },
    ],
    'outtmpl': save_yt_audio,
}   

ydl_opts_playlist = {
    'extract_flat': True,  # Do not download the videos, only extract information
    'skip_download': True,
}

resource_cp_files = [
    file_bookmarks,
    file_rename_list,
    file_comic_json,
    file_chapters,
    file_vol_chaps,
    file_yt_json,
    file_m3u8_mp4_json,
]

# Other constants
using_thread = True
