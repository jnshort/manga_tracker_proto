import bs4 as bs
import requests
import webbrowser
from pymongo import MongoClient
from tracked import tracked

db = MongoClient("mongodb://localhost:27017")
base_url = "https://ww7.mangakakalot.tv/"

class Manga():
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.ext = url[len(base_url):]
        




def ep_list_from_manga(manga):
    
