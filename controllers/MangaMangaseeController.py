import os
import requests
import json

from common.Constants import MANGASEE_DEBUG, file_sample_html, link_chapter_mangasee, prefix_chapter_folder
from common.Commons import generate_filename
from common.Messages import log_start_function, log_parameter, log_error, END_LOG
from common.Messages import MSG_ERR_CONTROLLER_MANGASEE

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
    if MANGASEE_DEBUG and DEBUG_OBJ["generate_chapter_link_mangasee"]:
        log_start_function("MangaMangaseeController", "generate_chapter_link_0000888mangasee")
        log_parameter("Chapter str", chapter_str, 1)

    try:
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

        if MANGASEE_DEBUG and DEBUG_OBJ["generate_chapter_link_mangasee"]:
            log_parameter("Result", result, 2)
            print(END_LOG)

        return result
    except Exception as e:
        if MANGASEE_DEBUG and DEBUG_OBJ["generate_chapter_link_mangasee"]:
            log_error("MangaMangaseeController", "generate_chapter_link_mangasee", e)
        raise Exception(MSG_ERR_CONTROLLER_MANGASEE.format("generate_chapter_link_mangasee"))

def generate_chapter_img(chapter_str: str) -> str:
    """
    Generate chapter image file name server mangasee123.com
    :param chapter_str: chapter to generate image file name
    :return: chapter image file name
    """
    
    # Debug print initial
    if MANGASEE_DEBUG and DEBUG_OBJ["generate_chapter_img"]:
        log_start_function("MangaMangaseeController", "generate_chapter_img")
        log_parameter("Chapter str", chapter_str, 1)

    try:
        chapter_str = str(chapter_str)
        chapter = chapter_str[1:-1]
        odd = chapter_str[-1]

        result = chapter if odd == "0" else chapter + "." + odd

        # Debug print result
        if MANGASEE_DEBUG and DEBUG_OBJ["generate_chapter_img"]:
            log_parameter("Result", result, 2)
            print(END_LOG)

        return result
    except Exception as e:
        if MANGASEE_DEBUG and DEBUG_OBJ["generate_chapter_img"]:
            log_error("MangaMangaseeController", "generate_chapter_img", e)
        raise Exception(MSG_ERR_CONTROLLER_MANGASEE.format("generate_chapter_img"))

def get_link_chapter_mangasee(link: str, num_chap: int = -1, start_idx: int = -1):
    """
    Get list of chapters from mangasee123
    :param link: link to get list of chapters
    :param num_chap: number of chapters to get
    :param start_idx: start index of the chapter
    :return: list of chapters
    """
    
    # Debug print initial
    if MANGASEE_DEBUG and DEBUG_OBJ["get_link_chapter_mangasee"]:
        log_start_function("MangaMangaseeController", "get_link_chapter_mangasee")
        log_parameter("Link", link, 1)
        log_parameter("Num chap", num_chap, 1)
        log_parameter("Start idx", start_idx, 1)

    list_chapters = []
    cur_path_name = ""
    index_name = ""
    link_splits = link.split('/')
    server = '/'.join(link_splits[:3])

    try:
      
        r = requests.get(link)

        f = open(file_sample_html, mode='w+', encoding='utf-8')
        f.write(r.text)
        f.close()

        chapters = []
        index_name = ""

        f = open(file_sample_html, mode='r+', encoding='utf-8')

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
        os.remove(file_sample_html)
        list_chapters = chapters

        if start_idx != -1:
            list_chapters = list_chapters[start_idx:]
        else: 
            list_chapters = list_chapters[::-1]
        
        if num_chap != -1:
            list_chapters = list_chapters[:num_chap]

        if start_idx == -1:
            list_chapters = list_chapters[::-1]
            
        # Debug print list_chapters
        if MANGASEE_DEBUG and DEBUG_OBJ["get_link_chapter_mangasee"]:
            log_parameter("List chapters", list_chapters, 2)
            print(END_LOG)

        return (server, list_chapters, cur_path_name, index_name)
        
    except Exception as e:
        if MANGASEE_DEBUG and DEBUG_OBJ["get_link_chapter_mangasee"]:
            log_error("MangaMangaseeController", "get_link_chapter_mangasee", e)
        raise Exception(MSG_ERR_CONTROLLER_MANGASEE.format("get_link_chapter_mangasee"))
    

def get_list_image_mangasee(index_name: str, chapter: dict):
    """
    Get list of images from mangasee123
    :param link: link to get list of images
    :param chapter: chapter to get list of images
    """ 
    
    # Debug print initial
    if MANGASEE_DEBUG and DEBUG_OBJ["get_list_image_mangasee"]:
        log_start_function("MangaMangaseeController", "get_list_image_mangasee")
        log_parameter("Index name", index_name, 1)
        log_parameter("Chapter", chapter, 1)

    try:
        id_chap_link = index_name + generate_chapter_link_mangasee(chapter["Chapter"])

        link = link_chapter_mangasee.format(id_chap_link)

        list_images = []

        r = requests.get(link)
        f_tmp = open(file_sample_html, 'w+', encoding='utf-8')
        f_tmp.write(r.text)
        f_tmp.close()
        f_tmp = open(file_sample_html, 'r+', encoding='utf-8')

        cur_path_name = ""
        for line in f_tmp.readlines():
            if "vm.CurPathName = " in line:
                cur_path_name = line.replace(
                    "vm.CurPathName = ", "").strip().replace(";", "").replace('"', "")
                break
        
        f_tmp.close()
        os.remove(file_sample_html)

        chap_name = f'{prefix_chapter_folder} {generate_chapter_img(chapter["Chapter"])}'

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
            
        # Debug print final
        if MANGASEE_DEBUG and DEBUG_OBJ["get_list_image_mangasee"]:
            log_parameter("List images", list_images, 2)
            print(END_LOG)

        return (chap_name, list_images)
    except Exception as e:
        if MANGASEE_DEBUG and DEBUG_OBJ["get_list_image_mangasee"]:
            log_error("MangaMangaseeController", "get_list_image_mangasee", e)
        raise Exception(MSG_ERR_CONTROLLER_MANGASEE.format("get_list_image_mangasee"))
    
    