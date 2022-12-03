
import os
import shutil
from icecream import ic

Volumes = [[1, 1, 4], [2, 5, 8], [3, 9, 12], [4, 13, 16], [5, 17, 21], [6, 22, 25], [7, 26, 29], [8, 30, 33], [9, 34, 37], [10, 38, 41], [11, 42, 45], [12, 46, 49], [13, 50, 53], [14, 54, 57], [
    15, 58, 61], [16, 62, 65], [17, 66, 69], [18, 70, 73], [19, 74, 78], [20, 79, 83], [21, 84, 87], [22, 88, 91], [23, 92, 95], [24, 96, 99], [25, 100, 103], [26, 104, 106], [27, 107, 108]]

tmpDir = os.listdir()

for volume in Volumes:
    print(volume[0])
    tmps = []
    for i in range(volume[1], volume[2]+1):
        print("Chap " + str(i))
        filenames = [x for x in tmpDir if "Chapter " + str(i) + " -" in x]
        print(filenames)
        tmps.extend(filenames)
    
    print(tmps)
    for i in tmps:
        shutil.move(i, "Fullmetal Alchemist - Vol"+ str(volume[0]),copy_function=shutil.copytree)

