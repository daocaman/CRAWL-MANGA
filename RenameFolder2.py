import os

chapter = []
f = open("chapter.txt", "r", encoding="utf-8")

for x in f:
    chapter.append(x)

chapter_new = []
f = open("chapter - Copy.txt", "r", encoding="utf-8")

for x in f:
    chapter_new.append(x)

for old, new in zip(chapter, chapter_new):
    if old!="chapter - Copy.txt\n" and old!="chapter.txt\n":
        os.rename(old.replace("\n", ""), new.replace("\n", ""))
