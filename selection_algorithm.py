from sqlalchemy import create_engine, insert, MetaData, Table, Column, String, text, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool
from itertools import combinations
from math import floor

engine = create_engine('sqlite:///recipes.db', connect_args={"check_same_thread": False}, poolclass=StaticPool)
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
            conn.execute(insert(recipes).values(name=i, ingredients=data[i][0][0], url=data[i][1], img=data[i][2]))
            conn.commit()

class recommendations:

    def __init__(self, inputs: list):
        self.inputs = inputs
    
    def combos_of_inputs(self):
        return sum([list(map(list, combinations(self.inputs, i))) for i in range(len(self.inputs)+1)], [])

    def recipe_selector(self):

        recommendations = []

        for combo in self.combos_of_inputs()[::-1]:
            if len(recommendations) >= 6:
                break
            else:
                st = ''
                nt = ''
                ft = ''

                for j in combo:
                    if combo.index(j) == len(combo)-1:
                        st+= f"'%{j}%'"
                    else:
                        st += f"'%{j}%' AND ingredients LIKE "

                for r in recommendations:
                    if len(recommendations) > 0:
                        ft = 'AND name !='

                    if recommendations.index(r) == len(recommendations)-1:
                        nt += f"'{r['name']}'"
                    else:
                        nt += f"'{r['name']}' OR "

                stmt = text(f"SELECT name, ingredients, url, img FROM recipes WHERE ingredients LIKE {st} {ft} {nt} LIMIT 6")
                res = engine.connect().execute(stmt)
                for i in res:
                    if len(recommendations) >= 6:
                        break
                    dict={}
          
                    dict['similarity'] = len(combo)/len(i.ingredients.split(" "))
                    dict["name"] = i.name
                    dict["url"] = i.url
                    dict["img"] = i.img

                    recommendations.append(dict)          

        return sorted(recommendations, key=lambda d: d['similarity'])[::-1]
