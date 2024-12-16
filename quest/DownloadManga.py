import questionary
from art import art
import os
import concurrent.futures

from common.Constants import manga_menu
from controllers.MangaMangaseeController import get_link_chapter_mangasee, get_list_image_mangasee
from controllers.MangaNettruyenController import get_link_chapter_nettruyen, get_list_image_nettruyen
from common.Commons import generate_filename
from controllers.DownloadImageController import download_image_process

error_message = f'{art("error")} Please enter a valid '

def quest_form_download_manga():
    # Link manga
    ques_link = f"Enter manga link: {art('gimme')}"
    
    while True:
        manga_link = questionary.text(ques_link).ask()
        
        if manga_link == "" or "https://" not in manga_link:
            print(error_message + "manga link")
            continue
        break
    
    # Select server
    ques_server = f"Select server: {art('gimme')}"
    server = questionary.select(ques_server, manga_menu).ask()
    server = manga_menu.index(server) + 1
    
    # Number of chapter
    ques_number_of_chapter = f"Enter number of chapter (optional): {art('gimme')}"
    while True:
        number_of_chapter = questionary.text(ques_number_of_chapter).ask()
        
        if number_of_chapter == "":
            number_of_chapter = -1
            break
        
        if not number_of_chapter.isdigit():
            print(error_message + "number of chapter")
            continue
        break
    
    # Start from index
    ques_start_from_index = f"Enter start from index (optional): {art('gimme')}"
    while True:
        start_from_index = questionary.text(ques_start_from_index).ask()
        if start_from_index == "":
            start_from_index = 1
            break
        
        if not start_from_index.isdigit():
            print(error_message + "start from index")
            continue
        break
    
    if server == 1:
        (server, list_chapters) = get_link_chapter_nettruyen(manga_link, number_of_chapter, start_from_index)
    else:
        (server, list_chapters, cur_path_name, index_name) = get_link_chapter_mangasee(manga_link, number_of_chapter, start_from_index)

    for chapter in list_chapters:
        if server == 1:
            (chapter_name, list_images) = get_list_image_nettruyen(chapter)
        else:
            (chapter_name, list_images) = get_list_image_mangasee(index_name, chapter)

        download_img_process = []

        for idx, img in enumerate(list_images):
            download_img_process.append({
                "link": img,
                "server": server,
                "file": os.path.join(chapter_name, generate_filename(idx=idx, ext=".jpg"))
            })

        if not os.path.exists(chapter_name):    
            os.mkdir(chapter_name)

        if os.cpu_count() > 1:
            with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() // 2) as executor:
                executor.map(download_image_process, download_img_process)
        else:
            for idx, img in enumerate(download_img_process):
                code_result = download_image_process(img)
               
    return manga_link, server, number_of_chapter, start_from_index