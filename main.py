import bs4 as bs
import requests
import webbrowser
from pymongo import MongoClient
from tracked import tracked
from constraints import *
from validators import *
db = MongoClient("mongodb+srv://justinshort01:1234@cluster0.ywbikr0.mongodb.net/").MangaCollection
#db = MongoClient("mongodb://localhost:27017").MangaCollection
base_url = "https://ww7.mangakakalot.tv"

def create():
    MongoClient("mongodb+srv://justinshort01:1234@cluster0.ywbikr0.mongodb.net/").drop_database("MangaCollection")
    db.create_collection("manga", **manga_validator)
    db.create_collection("chapters", **chapter_validator)
    for constraint in manga_constraints:
        db.manga.create_index(constraint, unique=True)
    for constraint in chapter_constraints:
        db.chapters.create_index(constraint, unique=True)


class Manga():
    def __init__(self, url):
        self.url = url
        self.name = self.get_title()
        self.current_chapter = 1
        self.chapters = []

        if db.manga.count_documents(self.query()) == 0:
            self.insert_manga()
        cnt = db.chapters.count_documents(self.query())
        for doc in db.chapters.find(self.query()):
            self.chapters.append(doc['_id'])
        self.get_chapters()


        

    def dict_rep(self):
        return {'name': self.name,
                'url': self.url,
                'current_chapter': self.current_chapter,
                'chapters': self.chapters}


    def query(self):
        """Returns a dict that can query for this manga in 
        the mangas collection"""
        return {'name': self.name}


    def get_next_chapter_num(self):
        """Returns an int that represents the chapter number 
        of the next chapter to be added."""
        return db.chapters.count_documents(self.query()) + 1



    def get_title(self):
        html_page = requests.get(self.url).text
        page = bs.BeautifulSoup(html_page, features="html.parser")
        title = ""

        for link in page.findAll('h1'):
            title = link.text 
        return title
    

    def get_chapters(self):
        for url_ext in self.ch_list():
            new_chapter = Chapter(self, base_url + url_ext, self.get_next_chapter_num())
            if db.chapters.count_documents(new_chapter.query()) == 0:
                new_chapter.insert_chapter()   
            

    def insert_manga(self):
        db.manga.insert_one(self.dict_rep())


    def ch_list(self):
        html_page = requests.get(self.url).text
        page = bs.BeautifulSoup(html_page, features="html.parser")
        chapters = []

        for link in page.findAll('a'):
            if link.get('href'):
                if link['href'].startswith("/chapter"):
                    chapters.append(link['href'])
        chapters.reverse()
        return chapters


class Chapter():
    def __init__(self, manga: Manga, url, chapter_number):
        self.manga = manga
        self.name = self.manga.name
        self.chapter_number = manga.get_next_chapter_num()
        self.read = False
        self.url = url


    def query(self):
        return {'name': self.name, 'chapter_number': self.chapter_number}


    def insert_chapter(self):
        db.chapters.insert_one(self.dict_rep())
        id = db.chapters.find_one(self.query())['_id']
        self.manga.chapters.append(id)
        chapters = {'$set': {'chapters': self.manga.chapters}}
        db.manga.update_one(self.manga.query(), chapters)
        

    def dict_rep(self):
        return {'name': self.name, 'chapter_number': self.chapter_number, 'url': self.url, 'read': self.read}


def main():
    link = tracked[0] 
    m1 = Manga(link)

main()



