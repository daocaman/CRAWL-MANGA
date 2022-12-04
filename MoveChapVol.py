import os
import shutil
from icecream import ic

def generateName(num, l):
    return "0"*(l - len(num))+num


keyword = ""

Volumes = [
    # [1, 1, 4],
    # [2, 5, 8],
    # [3, 9, 12],
    # [4, 13, 16],
    # [5, 17 , 20],
    # [6, 21, 24],
    # [7, 25, 28],
    # [8, 29, 32],
    # [9, 33, 36],
    # [10, 37, 40],
    # [11, 41, 44],
    [12, 45, 51],
    [13, 52, 55],
    [14, 56, 59],
    # [15, 60, 81],
    # [16, 73, 81],
    # [17, 73, 81],
]

tmpDir = os.listdir()

for volume in Volumes:
    tmps = []
    for i in range(volume[1], volume[2]+1):
        filenames = [x for x in tmpDir if "Chapter " +
                     generateName(str(i), 2) in x]
        tmps.extend(filenames)

    ic(tmps)
    for i in tmps:
        shutil.move(i, keyword+" - Vol" +
                    str(volume[0]), copy_function=shutil.copytree)
