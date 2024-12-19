import eel

from tasks.DownloadManga import main_process as download_manga_task
from tasks.ArchiveFolders import main_process as archive_manga_task
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

eel.start("index.html", size=(1200, 800)) 