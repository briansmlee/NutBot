# taken from http://www.rmunn.com/sqlalchemy-tutorial/tutorial.html
# sqlite connection for nutbot

import sqlite3
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///tutorial.db')

Base = declarative_base() 

class Foods(Base):
    __tablename__ = 'foods'
    
    id = Column(Integer, primary_key = True)
    name = Column(String)
    quantity = Column(Integer)
    calories = Column(Float)
    
    # optional
    def __repr__(self):
        return "<User(name=%s, quantity=%d, calories=%f>" % \
                self.name, self.quantity, self.calories

Base.metadata.create_all(engine)

ex_food = Foods(name='milk', quantity= 1, calories=120.0)

print(ex_food.name)

# create session
Session = sessionmaker(bind=engine)
session = Session()

# persist User obj by adding to Session
session.add(ex_food)
# now the instance is pending.

session.add_all([
    Foods(name='avocado', quantity=1, calories = 100.0)
])

session.commit()

print(ex_food.id)

for instance in session.query(Foods).order_by(Foods.id):
    print(instance.name, instance.quantity)
    



