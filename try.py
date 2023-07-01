import requests

link = 'https://uploads.mangadex.org/data/bca78b31209ae6e19c7be764a9336038/x9-43c385d3c14125c57c923b2d58649d911f8e392cadbefb36abb126f96120d5dd.png'

server = 'https://mangadex.org'

r = requests.get(link.replace("\n", ""), headers={
                    'User-agent': 'Mozilla/5.0', 'Referer': server}, timeout=(3, 5))

with open('test.jpg', "wb") as fd:
    if (r.status_code != 200):
        flag = True
    else:
        fd.write(r.content)