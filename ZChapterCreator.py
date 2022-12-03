import json
import re
import os
from icecream import ic
import shutil


def ArrFile(item):
    arrStartFile = re.split('[- _ .]', item["from"])
    arrEndFile = re.split('[- _ .]', item["to"])

    arr = []

    ic(arrStartFile)
    ic(arrEndFile)

    if len(arrStartFile) > 2:

        startIndex = int(arrStartFile[1])
        endIndex = int(arrEndFile[1])
        if len(arrStartFile) == 3:
            for i in range(startIndex, endIndex+1):
                tmp = arrStartFile[0] + "_"+(len(arrStartFile[1]) -
                                             len(str(i))) * "0" + str(i) + "." + arrStartFile[2]
                arr.append(tmp)

        else:
            for i in range(startIndex, endIndex+1):
                tmp = arrStartFile[0] + "-" + \
                    str(i) + "_" + arrStartFile[2] + "." + arrStartFile[3]
                arr.append(tmp)
    else:

        startIndex = int(arrStartFile[0])
        endIndex = int(arrEndFile[0])

        for i in range(startIndex, endIndex+1):

            tmp = (len(arrStartFile[0]) - len(str(i))) * \
                "0" + str(i) + "." + arrStartFile[1]

            arr.append(tmp)

    print(arr)
    return arr


f = None

if os.path.exists("zchapters.json"):
    f = open('zchapters.json', encoding='utf-8')
else:
    json_files = [pos_json for pos_json in os.listdir()
                  if pos_json.endswith('.json')]

    json_files.sort(reverse=True)

    if len(json_files) == 0:
        print("Error")
    else:
        f = open(json_files[0], encoding='utf-8')

if f != None:
    data = json.load(f)

    for item in data:

        if not os.path.exists(item["chapter_name"]):
            os.makedirs(item["chapter_name"])

        tmpArr = ArrFile(item)

        for file in tmpArr:
            if os.path.exists(file):
                shutil.move(file, item["chapter_name"]+"/"+file)
            else:
                ic("Check")
