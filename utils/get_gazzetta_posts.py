import feedparser
import requests
from bs4 import BeautifulSoup

from loader import db
from utils.run_blocking_io import run_blocking_io
from utils.translate import translate

rss_link = "https://www.gazzetta.it/rss/calcio.xml"


async def get_gazzetta_rss_links(rss=rss_link):
    print(f"Запрашиваем фид {rss}...")
    feed = feedparser.parse(rss)

    if feed.entries:
        links = [entry.link for entry in feed.entries]
        return links[::-1]
    else:
        return None


async def get_gazzetta_news(post):
    print(f"Обрабатываем пост {post}...")
    if post not in db.gazzetta_posts_links():
        responce = requests.get(post)
        print(f"Ответ сервера: {responce.status_code}")
        if responce.status_code == 200:
            soup = BeautifulSoup(responce.text, "html.parser")
            content = soup.find_all("div", class_="content")
            try:
                rawtext = " ".join(element.get_text() for element in content)
                if len(rawtext.split()):
                    print("Raw text:", rawtext)
                    print("Переводим...")
                    translation = translate(rawtext)
                    print("Translation: ", translation)
                    return rawtext, translation
                else:
                    return None, None
            except TypeError as err:
                print(err)
                return None, None
        else:
            return None, None
    else:
        return None, db.get_gazzetta_translation(post)

if __name__ == "__main__":
    print(get_gazzetta_rss_links())
