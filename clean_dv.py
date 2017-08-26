# script to clean usda and daily values csv files and join

import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import chardet

# determining file type due to encoding error
with open('daily_values.csv', 'rb') as f1:
    result = chardet.detect(f1.read())

dv_names = ['name', 'daily_values', 'extra'] # specifying cols to handle inconsistent col nums
dv = pd.read_csv('daily_values.csv', encoding=result['encoding'], names=dv_names)
dv = dv.drop(0) # remove first row due to repeated col names

dv_cleaned = dv['daily_values'].str.split(' ', 1, expand=True) # split dv into quantity, unit
dct = { 
        'name' : dv['name'],
        'quantity' : dv_cleaned[0],
        'unit' : dv_cleaned[1]
    }
dv = pd.DataFrame(dct)

def clean_unit(unit):
    if '(' in unit: # if unit is in parens, use it
        return unit.split('(')[1].split(')')[0] 
    elif ' ' in unit:
        return unit.split(' ', 1)[1]
    else:
        return unit

dv['unit'] = dv['unit'].apply(lambda x : clean_unit(x))
dv['quantity'] = dv['quantity'].apply(lambda x : x.replace(',', ''))

print('\n\n\n', dv)

##### now cleaning usda.csv

with open('usda.csv', 'rb') as f2:
    result = chardet.detect(f2.read())
usda = pd.read_csv('usda.csv', encoding=result['encoding']) # names=dv_names)
print(usda)

def isin_dv(usda_name, dv_names):
    for name in dv_names:
        if usda_name.lower() in name: # str pattern matching. NOT finding in list
            return True
    return False

# lower for case insensitive comparison
dv_names = [ name.lower() for name in dv['name'].tolist() ]
print(usda.loc[isin_dv(usda['name'], dv_names)])

