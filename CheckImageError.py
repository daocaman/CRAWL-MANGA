from os import listdir
from PIL import Image
from skimage import io
from icecream import ic
import os

f = open("error.txt", "w+", encoding="utf8")

for fol in listdir():
    if os.path.isdir(fol):
        for filename in listdir(fol):
            try:
                img = Image.open(fol+'/'+filename)  # open the image file
                img.verify()  # verify that it is, in fact an image
                img = io.imread(fol+'/'+filename)

            except Exception as e:
                ic(e)
                link_file = fol+'/' + filename
                ic(link_file)
                f.write(link_file)

f.close()
