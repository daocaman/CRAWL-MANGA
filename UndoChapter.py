from genericpath import isdir
import os
import shutil

count = 37

chapters = [1, 23, 41, 61, 81, 99, 117, 135, 153, 171]

for i in os.listdir():
    if(os.path.isdir(i)):
        for filename in os.listdir(i):
            print(i, ".jpg")
            shutil.move(i+"/" + filename, filename)
