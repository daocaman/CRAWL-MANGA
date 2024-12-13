import os
import requests
import json
from colorama import Fore, Style
from pprint import pprint
from common.Constants import MANGASEE_DEBUG
from common.Commons import generate_filename

DEBUG_OBJ = {
    "generate_chapter_link_mangasee": True,
    "generate_chapter_img": True,
    "get_link_chapter_mangasee": True,
    "get_list_image_mangasee": True,
}

def generate_chapter_link_mangasee(chapter_str: str) -> str:
    """
    Generate chapter link from server mangasee123.com
    :param chapter_str: chapter to generate link
    :return: chapter link
    """
    
    # Debug print initial   
    MANGASEE_DEBUG and DEBUG_OBJ["generate_chapter_link_mangasee"] and print(Fore.GREEN + '='*70 + Style.RESET_ALL)
    MANGASEE_DEBUG and DEBUG_OBJ["generate_chapter_link_mangasee"] and print(Fore.YELLOW + 'MangaMangaseeController: generate_chapter_link_mangasee'.center(70) + Style.RESET_ALL)
    MANGASEE_DEBUG and DEBUG_OBJ["generate_chapter_link_mangasee"] and print(Fore.BLUE + f'{"Chapter str:":<20}' + Style.RESET_ALL + f'{chapter_str: >49}')

    index = ""

    idexStr = int(chapter_str[0])

    if (idexStr != 1):
        index = '-index-' + idexStr

    chapter = int(chapter_str[1:-1])

    odd = ""

    odd_str = int(chapter_str[-1])

    if odd_str != 0:
        odd = "." + str(odd_str)

    result = "-chapter-" + str(chapter) + odd + index

    # Debug print result
    MANGASEE_DEBUG and DEBUG_OBJ["generate_chapter_link_mangasee"] and print(Fore.CYAN + f'{"Result:":<20}' + Style.RESET_ALL + f'{result: >49}')

    # Debug print final
    MANGASEE_DEBUG and DEBUG_OBJ["generate_chapter_link_mangasee"] and print(Fore.GREEN + '='*70 + Style.RESET_ALL)

    return result


def generate_chapter_img(chapter_str: str) -> str:
    """
    Generate chapter image file name server mangasee123.com
    :param chapter_str: chapter to generate image file name
    :return: chapter image file name
    """
    
    # Debug print initial
    MANGASEE_DEBUG and DEBUG_OBJ["generate_chapter_img"] and print(Fore.GREEN + '='*70 + Style.RESET_ALL)
    MANGASEE_DEBUG and DEBUG_OBJ["generate_chapter_img"] and print(Fore.YELLOW + 'MangaMangaseeController: generate_chapter_img'.center(70) + Style.RESET_ALL)
    MANGASEE_DEBUG and DEBUG_OBJ["generate_chapter_img"] and print(Fore.BLUE + f'{"Chapter str:":<20}' + Style.RESET_ALL + f'{chapter_str: >49}')

    chapter_str = str(chapter_str)
    chapter = chapter_str[1:-1]
    odd = chapter_str[-1]

    result = chapter if odd == "0" else chapter + "." + odd

    # Debug print result
    MANGASEE_DEBUG and DEBUG_OBJ["generate_chapter_img"] and print(Fore.CYAN + f'{"Result:":<20}' + Style.RESET_ALL + f'{result: >49}')

    # Debug print final
    MANGASEE_DEBUG and DEBUG_OBJ["generate_chapter_img"] and print(Fore.GREEN + '='*70 + Style.RESET_ALL)

    return result
    

def get_link_chapter_mangasee(link: str, num_chap: int = -1, start_idx: int = -1):
    """
    Get list of chapters from mangasee123
    :param link: link to get list of chapters
    :param num_chap: number of chapters to get
    :param start_idx: start index of the chapter
    :return: list of chapters
    """
    
    # Debug print initial
    MANGASEE_DEBUG and print(Fore.GREEN + '='*70 + Style.RESET_ALL)
    MANGASEE_DEBUG and print(Fore.YELLOW + 'MangaMangaseeController: get_link_chapter_mangasee'.center(70) + Style.RESET_ALL)
    MANGASEE_DEBUG and DEBUG_OBJ["get_link_chapter_mangasee"] and print(Fore.BLUE + f'{"Link:":<20}' + Style.RESET_ALL + f'{link: >49}')
    MANGASEE_DEBUG and DEBUG_OBJ["get_link_chapter_mangasee"] and print(Fore.BLUE + f'{"Num chap:":<20}' + Style.RESET_ALL + f'{num_chap: >49}')
    MANGASEE_DEBUG and DEBUG_OBJ["get_link_chapter_mangasee"] and print(Fore.BLUE + f'{"Start idx:":<20}' + Style.RESET_ALL + f'{start_idx: >49}')

    list_chapters = []
    link_splits = link.split('/')
    server = '/'.join(link_splits[:3])

    try:
      
        r = requests.get(link)

        f = open('test.html', mode='w+', encoding='utf-8')
        f.write(r.text)
        f.close()

        chapters = []
        index_name = ""

        f = open('test.html', mode='r+', encoding='utf-8')

        for line in f.readlines():
            if "vm.CurPathName = " in line:
                cur_path_name = line.replace("vm.CurPathName = ", "")

            if "vm.IndexName = " in line:
                index_name = line.replace("vm.IndexName = ", "")
                index_name = index_name.strip()
                index_name = index_name.replace(
                    '"', '').replace(";", "")

            if "vm.CHAPTERS =" in line:
                chapters = json.loads(line.replace(
                    'vm.CHAPTERS = ', "").replace(";", ""))
        
        f.close()
        os.remove('test.html')

        if start_idx != -1:
            list_chapters = list_chapters[start_idx:]
        else:
            list_chapters = list_chapters[::-1]
        
        if num_chap != -1:
            list_chapters = list_chapters[:num_chap]
            
        if start_idx != -1:
            list_chapters = list_chapters[::-1]
        
        # Debug print list_chapters
        MANGASEE_DEBUG and DEBUG_OBJ["get_link_chapter_mangasee"] and print(Fore.CYAN + f'{"List chapters:":<20}' + Style.RESET_ALL)
        MANGASEE_DEBUG and DEBUG_OBJ["get_link_chapter_mangasee"] and pprint(list_chapters)

        # Debug print final
        MANGASEE_DEBUG and DEBUG_OBJ["get_link_chapter_mangasee"] and print(Fore.GREEN + '='*70 + Style.RESET_ALL)

        return (server, list_chapters)
        
    except Exception as e:
        MANGASEE_DEBUG and DEBUG_OBJ["get_link_chapter_mangasee"] and print(Fore.RED + f'{"Error:":<20}' + Style.RESET_ALL + f'{e: >49}')
        MANGASEE_DEBUG and DEBUG_OBJ["get_link_chapter_mangasee"] and print(Fore.GREEN + '='*70 + Style.RESET_ALL)
        return (server, list_chapters)
    

def get_list_image_mangasee(index_name: str, chapter: dict):
    """
    Get list of images from mangasee123
    :param link: link to get list of images
    :param chapter: chapter to get list of images
    """ 
    
    # Debug print initial
    MANGASEE_DEBUG and DEBUG_OBJ["get_list_image_mangasee"] and print(Fore.GREEN + '='*70 + Style.RESET_ALL)    
    MANGASEE_DEBUG and DEBUG_OBJ["get_list_image_mangasee"] and print(Fore.YELLOW + 'MangaMangaseeController: get_list_image_mangasee'.center(70) + Style.RESET_ALL)
    MANGASEE_DEBUG and DEBUG_OBJ["get_list_image_mangasee"] and print(Fore.BLUE + f'{"Index name:":<20}' + Style.RESET_ALL + f'{index_name: >49}')
    MANGASEE_DEBUG and DEBUG_OBJ["get_list_image_mangasee"] and print(Fore.BLUE + f'{"Chapter:":<20}' + Style.RESET_ALL + f'{chapter: >49}')

    id_chap_link = index_name + generate_chapter_link_mangasee(chapter["Chapter"])

    link = "https://mangasee123.com/read-online/" + id_chap_link + ".html"

    list_images = []

    r = requests.get(link)
    f_tmp = open('test.html', 'w+', encoding='utf-8')
    f_tmp.write(r.text)
    f_tmp.close()
    f_tmp = open('test.html', 'r+', encoding='utf-8')

    cur_path_name = ""
    for line in f_tmp.readlines():
        if "vm.CurPathName = " in line:
            cur_path_name = line.replace(
                "vm.CurPathName = ", "").strip().replace(";", "").replace('"', "")
            break
    
    f_tmp.close()
    os.remove('test.html')

    chap_name = "Chapter " + generate_chapter_img(chapter["Chapter"])

    for p_idx in range(1, int(chapter["Page"])+1):
        img_link = "https://{curPathName}/manga/{index_name}/{directory}{img}.png"
        img_link = img_link.replace(
            "{curPathName}", cur_path_name)
        img_link = img_link.replace(
            "{index_name}", index_name)
        if chapter["Directory"] != "":
            img_link = img_link.replace(
                "{directory}", chapter["Directory"])
        else:
            img_link = img_link.replace(
                "{directory}", "")
        img_link = img_link.replace("{img}", generate_chapter_img(
            chapter["Chapter"])+"-"+ generate_filename(idx=p_idx, str_len=3))
        
        list_images.append(img_link)
        
    # Debug print list_images
    MANGASEE_DEBUG and DEBUG_OBJ["get_list_image_mangasee"] and print(Fore.CYAN + f'{"List images:":<20}' + Style.RESET_ALL)
    MANGASEE_DEBUG and DEBUG_OBJ["get_list_image_mangasee"] and pprint(list_images)

    # Debug print final
    MANGASEE_DEBUG and DEBUG_OBJ["get_list_image_mangasee"] and print(Fore.GREEN + '='*70 + Style.RESET_ALL)

    return (chap_name, list_images)
    
    