# Debug variables
COMMON_DEBUG = True


# Constants number
max_length_idx = 4

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