import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, select, insert, MetaData, Table, Column, String, text, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool
from itertools import combinations

engine = create_engine('sqlite:///recipes.db',connect_args={"check_same_thread": False}, 
    poolclass=StaticPool)
metadata = MetaData()
Base = declarative_base()

recipes = Table(
    "recipes",
    metadata,
    Column("name", String),
    Column("ingredients", String),
    Column("url", String),
    Column("img", String),
)

class Recipe(Base):
    __tablename__ = "recipes"
    name = Column("name", String)
    ingredients = Column("ingredients", String)
    url = Column("url", String, primary_key=True)
    img = Column("img", String)

def __repr__(self):
    return f'Recipe(name: {self.name}, ingredients: {self.ingredients}, url: {self.url}, img: {self.img}'

metadata.create_all(engine)

def Insert(data: dict):
    for i in data:
        with engine.connect() as conn:
            conn.execute(insert(recipes).values(name=i, ingredients=data[i][0], url=data[i][1], img=data[i][2]).prefix_with('OR IGNORE'))

class Scrape:

    recipe_data = {}

    def __init__(self, url: str, depth: int):
        self.url = url
        self.depth = depth

    def scrape_recipe(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        ingredient = soup.find_all('a', class_='glosslink')
        title = soup.select_one('div h1').string
        url = url
        img = soup.find_all('img', class_='recipe-hero-photo img-responsive')[0]['src']

        return {title: [(' '.join([ingredient[i].string for i in range(0,len(ingredient))])).lower(), url, img]}

    def search_depth(self):

        for i in range(1, self.depth+1):

            resp = requests.get(self.url[0:len(self.url)-1] + str(i))
            soup = BeautifulSoup(resp.content, 'html.parser')
            page_links = soup.find_all('div', class_='recipe-tile-full')
            links = [j.get('data-url') for j in page_links]

        for z in links:

            res = self.scrape_recipe(z)

            for k in res:

                self.recipe_data[k] = res[k]
