# sqlite connection for nutbot

import sqlite3

conn = sqlite3.connect('test.db')

print ("Opened DB successfully")

conn.execute('''CREATE TABLE FOODS
        (ID INT PRIMARY KEY NOT NULL,
        NAME TEXT NOT NULL,
        QUANTITY INT NOT NULL,
        CALORIES INT NOT NULL);''')

print ("Table created successfully")

def insert(db_id, name, quantity, calories)
conn.execute("INSERT INTO FOODS (ID, NAME, QUANTITY, CALORIES) \
        VALUES (

