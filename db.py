# taken from http://www.rmunn.com/sqlalchemy-tutorial/tutorial.html
# sqlite connection for nutbot

import sqlite3
import datetime
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

fmt = "%Y-%m-%d %H:%M:%S %Z"

engine = create_engine('sqlite:///ver1.db')

Base = declarative_base() 

# create session
Session = sessionmaker(bind=engine)
session = Session()


class Food(Base):
    __tablename__ = 'food'
    
    id = Column(Integer, primary_key = True)
    date_time = Column(DateTime)
    name = Column(String)
    quantity = Column(Integer)
    calories = Column(Float)
    user = Column(String)
    
    # optional
    def __repr__(self):
        return "<Food: datetime=%s name=%s, quantity=%d, calories=%f user=%s>" % \
                (self.date_time.strftime(fmt), self.name, self.quantity, self.calories, self.user)

Base.metadata.create_all(engine)

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

