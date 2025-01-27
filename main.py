import eel  
import os
import base64
import shutil

from tasks.DownloadManga import main_process as download_manga_task
from tasks.ArchiveFolders import main_process as archive_manga_task
from tasks.MoveChapVol import main_process as move_chapters_task
from tasks.CreateMetadata import main_process as create_metadata_task
from tasks.DownloadYT import main_process as download_yt_task
from tasks.DownloadCovers import main_process as download_covers_task
from tasks.ResizeImages import main_process as resize_images_task
from tasks.RenameFiles import main_process as rename_files_task
from tasks.CreateListFile import main_process as create_list_file_task
from tasks.RenameWithFile import main_process as rename_with_file_task
from tasks.ConvertTS import main_process as convert_ts_task
from tasks.DownloadM3U8 import main_process as download_m3u8_task
from common.Commons import init_app

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
    
@eel.expose
def download_yt(youtube_link, yt_type, is_playlist, file_yt, quality, is_convert):
    download_yt_task(youtube_link, yt_type, is_playlist, file_yt, quality, is_convert)
    eel.noLoadingScreen()
    eel.showMessage("Download youtube", "Youtube downloaded successfully")

@eel.expose
def download_cover(mangadex_url, number_of_covers):
    download_covers_task(mangadex_url, number_of_covers)
    eel.noLoadingScreen()
    eel.showMessage("Download cover", "Cover downloaded successfully")

@eel.expose
def resize_images(target_folder, is_multiple, is_horizontal):
    resize_images_task(target_folder, is_multiple, is_horizontal)
    eel.noLoadingScreen()
    eel.showMessage("Resize images", "Images resized successfully")

@eel.expose
def rename_files(target_folder, sort_files, start_index):
    rename_files_task(target_folder, sort_files, start_index)
    eel.noLoadingScreen()
    eel.showMessage("Rename files", "Files renamed successfully")

@eel.expose
def create_file_list(target_folder):
    create_list_file_task(target_folder)
    eel.noLoadingScreen()
    eel.showMessage("Create file list", "File list created successfully! Please edit file rename_list.json")

@eel.expose
def rename_files_with_file():
    rename_with_file_task()
    eel.noLoadingScreen()
    eel.showMessage("Rename files", "Files renamed successfully")
    
@eel.expose
def covert_ts(target_folder):
    convert_ts_task(target_folder)
    eel.noLoadingScreen()
    eel.showMessage("Convert ts", "Ts converted successfully")
    
@eel.expose
def download_m3u8(target_file):
    download_m3u8_task(target_file)
    eel.noLoadingScreen()
    eel.showMessage("Download m3u8", "M3u8 downloaded successfully")

@eel.expose
def load_f_e_images():
    folders = os.listdir()
    folders = [folder for folder in folders if os.path.isdir(folder) and folder.startswith("Chapter")]

    list_chaptes_images = []

    if os.path.exists("web/Chapters"):
        shutil.rmtree("web/Chapters")

    os.makedirs("web/Chapters", exist_ok=True)

    for folder in folders:
        files = os.listdir(folder)
        files.sort()
        current_chap = dict()
        current_chap["title"] = folder
        current_chap["start_page"] = files[0]
        current_chap["end_page"] = files[-1]
      
        target_folder = os.path.join("web/Chapters", folder)
        
        os.makedirs(target_folder, exist_ok=True)
        
        shutil.copy(os.path.join(folder, current_chap["start_page"]), target_folder)
        shutil.copy(os.path.join(folder, current_chap["end_page"]), target_folder)
        
        list_chaptes_images.append(current_chap)

    return list_chaptes_images

@eel.expose
def format_chapter(selected_chapters):
    for chapter in selected_chapters:
        info = chapter.split("_")
        chapter_name = info[0]
        page = info[1]

        current_file = os.path.join(chapter_name, page)
        os.remove(current_file)
    eel.noLoadingScreen()
    eel.showMessage("Format chapter", "Chapter formatted successfully")

if __name__ == "__main__":
    init_app()
    eel.start("index.html", size=(1200, 800))

