import os
from PIL import Image

from common.Constants import RESIZE_DEBUG
from common.Constants import verticle_size, horizontal_size
from common.Commons import is_image_file

def resize_image(folder='', is_horizontal=False):
    """
    Resize images in a folder
    :param folder: folder to resize images
    :param is_horizontal: resize images horizontally
    :return: None
    """

    # Debug print initial
    RESIZE_DEBUG and print("="*50)
    RESIZE_DEBUG and print('Common: resize_image')
    RESIZE_DEBUG and print(f"Folder: {folder}\nIs horizontal: {is_horizontal}")

    image_files = [f for f in os.listdir(folder) if is_image_file(f)]
    
    for  f in image_files:

        new_size = verticle_size
        
        image = Image.open(os.path.join(folder, f))

        width, height = image.size
        
        # Debug print width and height
        RESIZE_DEBUG and print(f"Old size: {width}x{height}")
        
        # Check if the image is horizontal
        if width > height or is_horizontal:
            new_size = horizontal_size
        
        # Debug print new size
        RESIZE_DEBUG and print(f"New size: {new_size}")

        resized_image = image.resize(new_size)
        resized_image.save(os.path.join(folder, f))

    # Debug print final
    RESIZE_DEBUG and print("="*50)
