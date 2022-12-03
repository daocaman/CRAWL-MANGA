import requests

links = []
f = open("error.txt", "r", encoding="utf8")


errFile = open("error - new.txt", "w+", encoding="utf8")
for x in f:
    print(x)
    links.append(x)

for img in links:

    spe = img.split(" - ")

    tmp = ""
    if len(spe) != 2:
        tmp =  spe[0:-1]
        print(tmp)
        tmp= " - ".join(tmp)
    else:
        tmp = spe[0]
    

    try:
        print(spe[-1].replace("\n", ""))
        r =requests.get(spe[-1].replace("\n", ""), headers={'User-agent': 'Mozilla/5.0', 'Referer': 'http://www.nettruyenpro.com/'})
        # r = requests.get(spe[-1].replace("\n", ""), headers={'User-agent': 'Mozilla/5.0', 'Connection': 'keep-alive', 'Referer': 'https: // readmanganato.com /'})

        print(tmp)
        with open(tmp, "wb") as fd:

            # fd.write(r.content)
            print(r.status_code)

            if(r.status_code != 200):
                errFile.write(img)
            else:
                fd.write(r.content)
    except Exception as e:
        print(e)
        errFile.write(img)
        continue
