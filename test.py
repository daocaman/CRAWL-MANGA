import requests
from bs4 import BeautifulSoup
from icecream import ic


link = "https://api.mangadex.org/manga/d97db976-eeec-4eb4-8868-346fbd7ed1e5?includes[]=artist&includes[]=author&includes[]=cover_art"
# link = "https://api.mangadex.org/manga/{manga_idx}?includes[]=artist&includes[]=author&includes[]=cover_art"

r = requests.get(link, headers={'User-agent': 'Mozilla/5.0'})

data = r.json()["data"]

title = data["attributes"]['title']
ic(title[list(title)[0]])

author = data["relationships"]

for rel in author:
    if rel['type'] == 'author':
        ic(rel['attributes']['name'])

# ic(title)
# ic(author)
