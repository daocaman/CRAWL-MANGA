import eel

from tasks.DownloadManga import main_process as download_manga_task
from tasks.ArchiveFolders import main_process as archive_manga_task
from tasks.MoveChapVol import main_process as move_chapters_task
from tasks.CreateMetadata import main_process as create_metadata_task
eel.init("web")

@eel.expose
def change_page(page):
    # Navigate to a different HTML file
    eel.show(f'{page}.html')

@eel.expose
def download_manga(manga_link, number_of_chapters, server, start_index):
    download_manga_task(manga_link, number_of_chapters, server, start_index)
    eel.noLoadingScreen()
    eel.showMessage("Download manga", "Manga downloaded successfully")

@eel.expose
def archive_manga(target_folder, multiple_folders, delete_folders):
    archive_manga_task(target_folder, multiple_folders, delete_folders)
    eel.noLoadingScreen()
    eel.showMessage("Archive manga", "Manga archived successfully")

@eel.expose
def move_chapters(folChaptersFile, mangaTitle, deleteAfterMove):
    move_chapters_task(folChaptersFile, mangaTitle, deleteAfterMove)
    eel.noLoadingScreen()
    eel.showMessage("Move chapters", "Chapters moved successfully")

@eel.expose
def create_metadata(bookmark_file, comic_info_file, target_folder, is_multiple_folders):
    create_metadata_task(bookmark_file, comic_info_file, target_folder, is_multiple_folders)
    eel.noLoadingScreen()
    eel.showMessage("Create metadata", "Metadata created successfully")

eel.start("index.html", size=(1200, 800)) 