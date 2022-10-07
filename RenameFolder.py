import os

f = open("chapter.txt", "w+", encoding="utf-8")
for file in os.listdir():
    f.write(os.fsdecode(file)+"\n")
