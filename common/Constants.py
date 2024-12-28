# Debug variables
COMMON_DEBUG = True
ARCHIVE_DEBUG = True
METADATA_DEBUG = True
NETTRUYEN_DEBUG = True
MANGASEE_DEBUG = True   
WEBCENTRAL_DEBUG = True
REFORMAT_DEBUG = True  
RESIZE_DEBUG = False
DOWNLOAD_COVERS_DEBUG = True
DOWNLOAD_MANGA_DEBUG = True
RENAME_DEBUG = True
DOWNLOAD_YOUTUBE_DEBUG = True
MOVE_CHAP_VOL_DEBUG = True
DOWNLOAD_NOVEL_DEBUG = True
LIST_AND_RENAME_DEBUG = True
DOWNLOAD_M3U8_DEBUG = True
CONVERT_TS_DEBUG = True

# Constants number
max_length_idx = 4
max_download_trial = 3

# Constants string
file_prefix = "pages_"
server_mangasee = "https://mangasee123.com"
server_nettruyen = "https://nettruyenviet.com"
server_mangadex = "https://mangadex.org"
chapter_folder_prefix = "Chapter"

api_cover = "https://api.mangadex.org/cover?order[volume]=asc&manga[]={0}&limit=100&offset={1}"
link_cover ="https://uploads.mangadex.org/covers/{0}/{1}"

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

# file name
file_bookmarks = "Bookmarks.json"
file_comic_json = "ComicInfo.json"
file_comic_xml = "ComicInfo.xml"
file_chapters = "Chapters.json"
cover_folder = "Covers"
manga_vol = "{0} - Vol{1}"

# example objects
bookmark_obj = {
    "title": "",
    "page": 0,
}

header_obj = {
    'User-agent': 'Mozilla/5.0', 
    'Referer': ""
}

horizontal_size = (1448, 1072)
verticle_size = (1072, 1448)

ydl_opts_video = {
    'format': 'bestvideo[height<=720]+bestaudio/best',  # Download the best quality video and audio with resolution 1080 or less
    'outtmpl': '%(title)s.%(ext)s',  # Output filename format (video and audio will have the same title)
}

ydl_opts_audio = {
    'format': 'bestaudio/best',  # Download the best quality audio
    # 'postprocessors': [
    #     {
    #         'key': 'FFmpegExtractAudio',  # Correct key for extracting audio
    #         'preferredcodec': 'mp3',  # Convert audio to mp3 format
    #         'preferredquality': '192',  # Set the preferred quality to 192 kbps
    #     },
    # ],
    'outtmpl': '%(title)s.%(ext)s',  # Output filename format
}   

ydl_opts_playlist = {
    'extract_flat': True,  # Do not download the videos, only extract information
    'skip_download': True,
}

save_yt_audio = "yt_audio/%(title)s.%(ext)s"
save_yt_video = "yt_video/%(title)s.%(ext)s"

page_break = "※----*-------⁛-------*----※"

sstruyen_link = "https://sstruyen.vn/{0}/chuong-{1}"

rename_list_file = "resource/rename_list.json"

save_m3u8_file = "m3u8"
