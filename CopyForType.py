import os
import shutil

if not os.path.exists("Reading"):
    os.mkdir("Reading")

count = 0

def getKey(x):
    tmp = x.split(".")[0]
    tmp = tmp.split("_")[-1]
    return int(tmp)
  
for fol in os.listdir():
    if os.path.isdir(fol) and fol != "Reading":
        count +=1
        files = os.listdir(fol)
        files = sorted(files, key=getKey)
        shutil.copy(fol+"/"+files[0], "Reading/"+str(count)+".jpg")
        if len(files) !=1:
            count +=1
            shutil.copy(fol+"/"+files[-1], "Reading/"+str(count)+".jpg")

