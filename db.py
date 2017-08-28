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
    # food_id = Column(String)
    quantity = Column(Integer)
    calories = Column(Float) # move to food table?
     
    # optional
    def __repr__(self):
       return "<Food: datetime=%s name=%s, quantity=%d, calories=%f user=%s>" % \
               (self.date_time, self.food_name, self.quantity, self.calories, self.user)
                

##### mapping food table to class
# uses dynamic column gen
class Food(object):
    # def __init__(self, food_dct):
    pass

dv_file = open('./dv.csv')
dvReader = csv.DictReader(dv_file)

food_table = Table('food', metadata,
        Column('id', Integer, primary_key=True),
        Column('food_name', String)
        # Column('food_id', String),
        # dynamic column generation from daily value columns
        # use attr_id or name?
        *(Column(nutrition['name'], Float) for nutrition in dvReader)
        )

metadata.create_all() # creates table
mapper(Food, food_table)

def db_add_consumption(dct, user):
    # mthd currently assumes input data fmt matches col names.
    # need a way to reformat here?
    dct['user'] = user
    cons = Consumption(**dct) # unfolds dict
    session.add(cons)
    session.commit()

def db_add_food(dct, food_id):
    dct['food_id'] = food_id
    food = Food(**dct)
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

