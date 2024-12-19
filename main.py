import eel

from tasks.DownloadManga import main_process as download_manga_task

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

eel.start("main.html", size=(1200, 800)) 