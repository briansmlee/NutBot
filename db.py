# taken from http://www.rmunn.com/sqlalchemy-tutorial/tutorial.html
# sqlite connection for nutbot

import sqlite3
import datetime
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper, session
import csv

fmt = "%Y-%m-%d %H:%M:%S %Z" #dateTime format

# session connects to engine for resources
engine = create_engine('sqlite:///ver2.db') 
# create session
Session = sessionmaker(bind=engine)
session = Session()
# use declarative base
Base = declarative_base() 
metadata = MetaData(bind=engine)

class Consumption(Base):
    __tablename__ = 'Consumption'
     
    id = Column(Integer, primary_key = True)
    date_time = Column(DateTime) # when ate
    user = Column(String) # who ate
    food_name = Column(String) 
    food_id = Column(String)
    quantity = Column(Integer)
    calories = Column(Float) # move to food table?
     
    # optional
    # def __repr__(self):
    #    return "<Food: datetime=%s name=%s, quantity=%d, calories=%f user=%s>" % \
                

##### mapping food table to class

class Food(object):
    # def __init__(self, food_dct):
    pass

dv_file = open('./dv.csv')
dvReader = csv.DictReader(dv_file)
for n in dvReader:
    print(n)

food_table = Table('food', metadata,
        Column('id', Integer, primary_key=True),
        Column('food_id', String),
        # dynamic column generation from daily value columns
        # use attr_id or name?
        *(Column(nutrition['name'], Integer) for nutrition in dvReader)
        )


metadata.create_all() # creates table
mapper(Food, food_table)
# session = create_session(bind=engine, autocommit=False, autoFlush=True)
# Base.metadata.create_all(engine)

def db_add_food(dct, user):
    dct['user'] = user
    food = Food(**dct) # unfolds dict
    session.add(food)
    session.commit()
    
def db_all_foods(users):
    """get all rows rel to input users"""
    # for instance in session.query(Food).order_by(Food.id):
    #    print(instance) # ok?


def db_daily_summary():
    today = datetime.datetime.now()
    start = today.replace(hour=0, minute=0, second=0)
    
    for food in session.query(Food).filter(Food.date_time > start).order_by(Food.id):
        print(food)

