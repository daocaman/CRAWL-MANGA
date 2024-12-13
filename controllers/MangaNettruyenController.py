import requests
from bs4 import BeautifulSoup

from common.Constants import NETTRUYEN_DEBUG, chapter_folder_prefix
from common.Commons import generate_filename

DEBUG_OBJ = {
    "get_link_chapter_nettruyen": True,
    "get_list_image_nettruyen": True,
}

def get_link_chapter_nettruyen(link= '', num_chap = -1, start_idx = -1):
    """
    Get list of chapters from nettruyen
    :param link: link to get list of chapters
    :param num_chap: number of chapters to get
    :param start_idx: start index of the chapter
    :return: list of chapters
    """
    
    # Debug print initial
    NETTRUYEN_DEBUG and DEBUG_OBJ["get_link_chapter_nettruyen"] and print("="*50)
    NETTRUYEN_DEBUG and DEBUG_OBJ["get_link_chapter_nettruyen"] and print('Common: get_link_chapter_nettruyen')
    NETTRUYEN_DEBUG and DEBUG_OBJ["get_link_chapter_nettruyen"] and print(f"Link: {link}\nNum chap: {num_chap}\nStart idx: {start_idx}")

    list_chapters = []
    link_splits = link.split('/')
    server = '/'.join(link_splits[:3])

    container_chapters = "nt_listchapter"
    ul_id = "desc"

    try:
        r = requests.get(link, headers={
            'User-agent': 'Mozilla/5.0'}, timeout=(3, 5))
        
        htmlSource = r.content
        soup = BeautifulSoup(htmlSource, 'html.parser')

        container_chapters_ele = soup.find(id=container_chapters)
        ul_ele = container_chapters_ele.find(id=ul_id)
        a_eles = ul_ele.find_all('a')

        list_chapters = [a['href'] for a in a_eles]
        
        if start_idx != -1:
            list_chapters = list_chapters[start_idx:]
        else:
            list_chapters = list_chapters[::-1]
            
        if num_chap != -1:
            list_chapters = list_chapters[:num_chap]
            
        if start_idx != -1:
            list_chapters = list_chapters[::-1]
            
        # Debug print list_chapters
        NETTRUYEN_DEBUG and DEBUG_OBJ["get_link_chapter_nettruyen"] and print(f"List chapters: \n{'\n'.join(list_chapters)}")

        # Debug print final
        NETTRUYEN_DEBUG and DEBUG_OBJ["get_link_chapter_nettruyen"] and print("="*50)

        return (server, list_chapters)
        
    except Exception as e:
        NETTRUYEN_DEBUG and DEBUG_OBJ["get_link_chapter_nettruyen"] and print(f"Error: {e}")
        return (server, list_chapters)
    

def get_list_image_nettruyen(link=''):
    """
    Get list of images from nettruyen
    :param link: link to get list of images
    """
    
    # Debug print initial
    NETTRUYEN_DEBUG and DEBUG_OBJ["get_list_image_nettruyen"] and print("="*50)
    NETTRUYEN_DEBUG and DEBUG_OBJ["get_list_image_nettruyen"] and print('Common: get_list_image_nettruyen')
    NETTRUYEN_DEBUG and DEBUG_OBJ["get_list_image_nettruyen"] and print(f"Link: {link}")

    list_images = []
    
    title = "Not found"
    
    image_src_atrs = ["data-src", "data-sv1", "data-sv2"]

    div_images = ["page-chapter"]

    try:
        r = requests.get(link, headers={
            'User-agent': 'Mozilla/5.0'}, timeout=(3, 5))
        
        htmlSource = r.content
        soup = BeautifulSoup(htmlSource, 'html.parser')

        title = soup.find('title')
        title = title.text.split(" Next Chap ")[0].strip()

        chap = title.split(" ")[-1]
        odd = -1
        if len(chap.split(".")) >= 2:
            odd = chap.split(".")[-1]
            chap = chap.split(".")[0]

        title = f"{chapter_folder_prefix} {generate_filename(idx=int(chap))}"

        if odd != -1:
            title = f"{title}.{odd}"

        div_images_ele = []
        for div_image in div_images:
            div_images_ele = soup.find_all('div', class_=div_image)
            if len(div_images_ele) > 0:
                break
        
        for div_image_ele in div_images_ele:
            img_ele = div_image_ele.find('img')
            for atr in image_src_atrs:
                if atr in img_ele.attrs:
                    list_images.append(img_ele[atr])
                    break

        list_images = [f if 'https' in f else "https://" + f  for f in list_images ]

        # Debug print list_images
        NETTRUYEN_DEBUG and DEBUG_OBJ["get_list_image_nettruyen"] and print(f"List images: \n{'\n'.join(list_images)}")

        # Debug print final
        NETTRUYEN_DEBUG and DEBUG_OBJ["get_list_image_nettruyen"] and print("="*50)

        return (title, list_images)
        
    except Exception as e:
        NETTRUYEN_DEBUG and DEBUG_OBJ["get_list_image_nettruyen"] and print(f"Error: {e}")
        return (title, list_images)
    
