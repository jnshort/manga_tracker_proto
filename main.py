import bs4 as bs
import requests
import webbrowser
from pymongo import MongoClient
from tracked import tracked
from password import password
db = MongoClient("mongodb+srv://justinshort01:{password}@cluster0.ywbikr0.mongodb.net/")
#db = MongoClient("mongodb://localhost:27017")
base_url = "https://ww7.mangakakalot.tv/"

class Manga():
    def __init__(self, name, url):
        self.url = url
        self.url = self.get_title()
        self.ext = url[len(base_url):]
        self.current_chapter = 0
        
    def query(self):
        """Returns a dict that can query for this manga in 
        the mangas collection"""
        return {'name': self.name}

    def get_next_chapter_num(self):
        """Returns an int that represents the chapter number 
        of the next chapter to be added."""
        return db.chapters.count_documents(self.query) + 1

    def get_title(self):
        html_page = requests.get(url).text
        page = bs.BeautifulSoup(html_page, features="html.parser")
        title = ""

        for link in page.findAll('h1'):
            title = link.text 
        return title
    
    def get_chapters(self):
        
        

class Chapter():
    def __init__(self, manga: Manga, url):
        self.manga = manga.query()
        self.name = self.manga.name
        self.chapter_number = manga.get_next_chapter_num()
        self.watched = False

class Test:
    def __init__(self, url):
        self.url = url


def ep_list_from_manga(manga):
    html_page = requests.get(manga.url).text
    page = bs.BeautifulSoup(html_page, features="html.parser")
    chapters = []

    for link in page.findAll('a'):
        if link.get('href'):
            if link['href'].startswith("/chapter"):
                chapters.append(link['href'])
    chapters.reverse()
    return chapters



def main():
    manga = "https://ww7.mangakakalot.tv/manga/manga-ut997828"    
    get_title(manga)
main()



