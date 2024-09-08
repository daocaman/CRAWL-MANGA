import re
import os
import shutil
import json
import requests
from icecream import ic
from PIL import Image
from skimage import io

from Constants import COMMON_DEBUG

# constants number
from Constants import max_length_idx

# constants string
from Constants import file_prefix

# constants files
from Constants import file_comic_xml, file_chapters

# content of the file
from Constants import comic_xml, comic_series, comic_writer, comic_volume, comic_summary, comic_page, comic_pages_op, comic_pages_cl

# constants objects
from Constants import horizontal_size, verticle_size, bookmark_obj

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
    result_str = result_str[-str_len:]
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
