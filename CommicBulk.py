import os


def takeKey(elem):
    tmp = elem.split("Vol")[1]
    return int(tmp)


start = 1  # start volume
end = 23  # end volume

excepts = []

title = "Conan"

author = "Gosho AOYAMA"

# stage 1: have description and start end volume
# stage 2: no description
# stage 3: have description (no start, end vol)

stage = 2

# Volume titles
description = [

]

xmlContaint = "<?xml version=\"1.0\" encoding=\"utf-8\"?>" +\
    "<ComicInfo xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">" +\
    "{content}" +\
    "</ComicInfo>"

xmls = []

if stage == 1:

    for i, desc in enumerate(description):
        series = "<Series>"+title+"</Series>\n"
        volume = "<Volume>"+str(i+1)+"</Volume>\n"
        writer = "<Writer>"+author+"</Writer>\n"
        sumary = "<Summary>"+desc+"</Summary>"
        final = ''+xmlContaint
        final = final.replace("{content}", series+volume+writer+sumary)
        xmls.append(final)
elif stage == 2:
    for i in range(start, end+1):
        if i not in excepts:
            series = "<Series>"+title+"</Series>\n"
            volume = "<Volume>"+str(i)+"</Volume>\n"
            writer = "<Writer>"+author+"</Writer>\n"
            final = ''+xmlContaint
            final = final.replace("{content}", series+volume+writer)
            xmls.append(final)
else:
    for i, desc in enumerate(description):
        series = "<Series>"+title+"</Series>\n"
        volume = "<Volume>"+str(start+i)+"</Volume>\n"
        writer = "<Writer>"+author+"</Writer>\n"
        sumary = "<Summary>"+desc+"</Summary>"
        final = ''+xmlContaint
        final = final.replace("{content}", series+volume+writer+sumary)
        xmls.append(final)

index = 0


listFiles = os.listdir()

listFiles.remove("ArchiveBulk.py")
listFiles.remove("CommicBulk.py")

print(listFiles)

listFiles = sorted(listFiles, key=takeKey)

# print(listFiles)

for fol in listFiles:
    print(fol)
    if os.path.isdir(fol):
        f = open(fol+"/"+"ComicInfo.xml", "w+", encoding="utf8")
        f.write(xmls[index])
        f.close()
        index += 1
