import re
import os
import shutil
import json
import requests
from icecream import ic
from PIL import Image
from skimage import io
from bs4 import BeautifulSoup
from lxml import html

from Constants import COMMON_DEBUG

# constants number
from Constants import max_length_idx

# constants string
from Constants import file_prefix, chapter_folder_prefix

# constants files
from Constants import file_comic_xml, file_chapters

# content of the file
from Constants import comic_xml, comic_series, comic_writer, comic_volume, comic_summary, comic_page, comic_pages_op, comic_pages_cl

# constants objects
from Constants import horizontal_size, verticle_size, bookmark_obj, header_obj

def is_image_file(file_name=''):
    """
    Check if a file is an image file
    :param file_name: file name to check
    :return: True if the file is an image file, False otherwise
    """
    ext = file_name.split('.')[-1]

    return ext in ['jpg', 'png', 'jpeg']


def generate_filename(prefix='', idx=0, ext='', str_len=max_length_idx):
    """
    Generate a filename with a specific format
    :param prefix: prefix of the filename
    :param idx: index of the filename
    :param ext: extension of the filename
    :param str_len: length of the index
    :return: a filename with the format: prefix + index + ext
    """
    result_str = "0"*str_len + str(idx)
    result_str = result_str[-1*str_len:]
    COMMON_DEBUG and ic(result_str)
    return f'{prefix}{result_str}{ext}'


def extract_number(s='', last=False):
    """
    Extract number from a string
    :param s: input string
    :return: a number extracted from the string
    """
    if last:
        match = re.findall(r'\d+', s)
        return int(match[-1]) if match else 0
    
    match = re.search(r'\d+', s)
    return int(match.group()) if match else 0


def generate_metadata(series, writer, vol=-1, table_content=[], summary="", target_folder=""):
    """
    Generate metadata for a comic
    :param series: series of the comic
    :param writer: writer of the comic
    :param vol: volume of the comic
    :param table_content: tablecontent of the comic
    :param summary: summary of the comic
    :param target_folder: target folder to save the metadata file
    :return: None
    """

    COMMON_DEBUG and ic(f"Generate metadata for {target_folder}")

    xml_containt = comic_xml

    metas = []
    metas.append(comic_series.format(series))
    metas.append(comic_writer.format(writer))

    # add volume information
    if vol != -1:
        metas.append(comic_volume.format(vol))

    # add summary information
    if summary != "":
        metas.append(comic_summary.format(summary))

    # add bookmark information
    if len(table_content) > 0:
        metas.append(comic_pages_op)
        for content in table_content:
            metas.append(comic_page.format(
                content['page'], content['title']))
        metas.append(comic_pages_cl)

    final = xml_containt.format(content="\n".join(metas))

    f = open(os.path.join(target_folder, file_comic_xml),
             "w+", encoding="utf8")
    f.write(final)
    f.close()


def archive_folder(folder='', is_delete=False):
    """
    Archive a folder
    :param folder: folder to archive
    :param is_delete: delete the folder after archiving
    :return: None
    """
    COMMON_DEBUG and ic(f"Archive {folder}.zip")
    if os.path.exists(f'{folder}/{file_chapters}'):
        os.remove(f'{folder}/{file_chapters}')

    shutil.make_archive(folder, "zip", base_dir=folder)
    if is_delete:
        shutil.rmtree(folder)


def resize_image(folder='', is_horizontal=False):
    """
    Resize images in a folder
    :param folder: folder to resize images
    :param is_horizontal: resize images horizontally
    :return: None
    """

    COMMON_DEBUG and ic(f"Resize images in {folder}")

    image_files = [f for f in os.listdir(folder) if is_image_file(f)]
    
    for  f in image_files:

        new_size = verticle_size
        
        image = Image.open(os.path.join(folder, f))

        width, height = image.size
        if width > height or is_horizontal:
            new_size = horizontal_size

        resized_image = image.resize(new_size)
        resized_image.save(os.path.join(folder, f))


def reformat_folder(folder='', is_delete=False):
    """
    Reformat a folder
    :param folder: folder to reformat
    :param is_delete: delete chapter folders
    :return: None
    """

    COMMON_DEBUG and ic(f"Reformat {folder}")
    count = 0
    folders = os.listdir(folder)
    folders = [f for f in folders if os.path.isdir(os.path.join(folder,f))]
    folders = sorted(folders, key=lambda x: extract_number(x, True))
    list_chapters = []
    for fol in folders:
        list_chapters.append({
            "title": fol,
            "page": count
        })
        images = os.listdir(os.path.join(folder, fol))
        images = [f for f in images if is_image_file(f)]
        images = sorted(images, key=lambda x: extract_number(x))

        for img in images:
            new_name = generate_filename(file_prefix, count, ".jpg")
            shutil.copy(os.path.join(folder, fol, img),
                        os.path.join(folder, new_name))
            count += 1
        
        if is_delete:
            shutil.rmtree(os.path.join(folder, fol))

    with open(os.path.join(folder, file_chapters), 'w+', encoding="utf-8") as json_file:
        # Write the list to the file
        json.dump(list_chapters, json_file, ensure_ascii=False, indent=4)


def check_image_error(filename=''):
    """
    Check image error
    :param filename: filename to check
    :return: None
    """
    COMMON_DEBUG and ic(f"Check image error in {filename}")
    try:
        img = Image.open(filename)  # open the image file
        img.verify()  # verify that it is, in fact an image
        img = io.imread(filename)
    except Exception as e:
        COMMON_DEBUG and ic(e)
        return False
    
    return True
        

def download_image(link: str, server: str, file: str, count: int):
    """
    Download image from link
    :param link: link to download
    :param server: server to download
    :param file: file to save
    :param count: count to download
    :return: return status code
    """

    if os.path.exists(file):

        # Check file exist and is a valid image
        # if image valid return 200
        # else remove file and download again until count = 3

        if not check_image_error(file):
            os.remove(file)
            if count < 3:
                return download_image(link, server, file, count+1)
        else:
            return 200

    else:
        if count < 3:
            try:
                r = requests.get(link.replace("\n", ""), headers={
                    'User-agent': 'Mozilla/5.0', 'Referer': server}, timeout=(3, 5))

                down_faied = False  # Check download success or not
                down_code = 200
                with open(file, "wb") as fd:
                    down_code = r.status_code
                    if (down_code != 200):
                        down_faied = True
                    else:
                        fd.write(r.content)

                if down_faied:
                    # If download fail and status code is not 404
                    # true: remove file and download again until count = 3
                    # false: return 404
                    if down_code == 404:
                        os.remove(file)
                        return 404
                    return download_image(link, server, file, count+1)
                else:
                    return download_image(link, server, file, count)
            except Exception as e:
                COMMON_DEBUG and print("Error: ", e)
                return 400


def get_link_chapter_nettruyen(link= '', num_chap = -1):
    """
    Get list of chapters from nettruyen
    :param link: link to get list of chapters
    :param num_chap: number of chapters to get
    :return: list of chapters
    """
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

        if num_chap == -1:
            list_chapters = [a['href'] for a in a_eles]
        else:
            list_chapters = [a['href'] for a in a_eles[:num_chap]]
        
        return (server, list_chapters[::-1])
        
    except Exception as e:
        COMMON_DEBUG and ic(e)
        return (server, list_chapters)
    

def get_list_image_nettruyen(link=''):
    """
    Get list of images from nettruyen
    :param link: link to get list of images
    """

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

        return (title, list_images)
        
    except Exception as e:
        COMMON_DEBUG and ic(e)
        return (title, list_images)
    

def generate_chapter_link_mangasee(chapter_str: str) -> str:
    """Generate chapter link from server mangasee123.com"""
    index = ""

    idexStr = int(chapter_str[0])

    if (idexStr != 1):
        index = '-index-' + idexStr

    chapter = int(chapter_str[1:-1])

    odd = ""

    odd_str = int(chapter_str[-1])

    if odd_str != 0:
        odd = "." + str(odd_str)

    return "-chapter-" + str(chapter) + odd + index


def generate_chapter_img(chapter_str: str) -> str:
    """Generate chapter image file name server mangasee123.com"""
    chapter_str = str(chapter_str)
    chapter = chapter_str[1:-1]
    odd = chapter_str[-1]

    if odd == "0":
        return chapter
    else:
        return chapter + "." + odd
    

def get_link_chapter_mangasee(link: str, num_chap: int):
    """
    Get list of chapters from mangasee123
    :param link: link to get list of chapters
    :param num_chap: number of chapters to get
    :return: list of chapters
    """
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

        return (server, chapters[-num_chap:], cur_path_name, index_name)
        
    except Exception as e:
        COMMON_DEBUG and ic(e)
        return (server, list_chapters)
    

def get_list_image_mangasee(index_name: str, chapter: dict):
    """
    Get list of images from mangasee123
    :param link: link to get list of images
    :param chapter: chapter to get list of images
    """ 
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
    
    return (chap_name, list_images)
    
    
def get_info_chapter(link: str, xpath: str, is_list = True, list_item_ele = ''):
    r = requests.get(link, headers=header_obj, timeout=(3, 5))
    tree = html.fromstring(r.content)

    ic(tree.xpath(xpath))

    if not is_list:
        ic(tree.xpath(xpath+"/text()"))
        return tree.xpath(xpath+"/text()")
    else:
        chapters = tree.xpath(xpath + f"//{list_item_ele}")

        # get text from each element in the list
        for chap in chapters:
            tmp_text = chap.xpath(".//text()")
            tmp_text = "".join(tmp_text)
            if tmp_text != "":
                ic(tmp_text)

        
