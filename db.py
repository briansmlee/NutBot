# taken from http://www.rmunn.com/sqlalchemy-tutorial/tutorial.html
# sqlite connection for nutbot

import sqlite3
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

fmt = "%Y-%m-%d %H:%M:%S %Z"


engine = create_engine('sqlite:///tutorial1.db')

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
    
    # optional
    def __repr__(self):
        return "<Food: datetime=%s name=%s, quantity=%d, calories=%f>" % \
                (self.date_time.strftime(fmt), self.name, self.quantity, self.calories)


Base.metadata.create_all(engine)

def db_add_food(dct):
    food = Food(**dct) # unfolds dict
    session.add(food)
    session.commit()
    
def db_all_foods():
    for instance in session.query(Food).order_by(Food.id):
        print(instance) # ok?

