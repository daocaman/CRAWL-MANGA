import os
import shutil
import re

def takeKey(elem):
    tmp = elem.split(".")[0]
    tmp = re.split(" |_",tmp)
    return int(tmp[len(tmp)-1])

coverFolderTxt = "Duel master"

prefix = "Duel Master"

listFiles = os.listdir(coverFolderTxt)

listFiles = sorted(listFiles, key=takeKey)

# print(listFiles)

for idx, cover in enumerate(listFiles):

    extFile = cover.split(".")[1]

    if not os.path.exists(prefix+" - Vol"+str(idx+1)):
        os.mkdir(prefix+" - Vol"+str(idx+1))
    if not os.path.exists(prefix+" - Vol"+str(idx+1)+"/00_Cover"):
        os.mkdir(prefix+" - Vol"+str(idx+1)+"/00_Cover")

    shutil.copyfile(coverFolderTxt+"/"+cover, prefix+" - Vol"+str(idx+1) +
                    "/00_Cover"+"/"+"0000"+"."+extFile)
