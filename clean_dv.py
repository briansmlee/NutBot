# script to clean usda and daily values csv files and join

import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import chardet

# determining file type due to encoding error
with open('daily_values.csv', 'rb') as f1:
    result = chardet.detect(f1.read())

dv_names = ['name', 'daily_values', 'attr_id'] # specifying cols to handle inconsistent col nums
dv = pd.read_csv('daily_values.csv', encoding=result['encoding'], names=dv_names)
dv = dv.drop(0) # remove first row due to repeated col names

dv_cleaned = dv['daily_values'].str.split(' ', 1, expand=True) # split dv into quantity, unit
dct = { 
        'name' : dv['name'],
        'quantity' : dv_cleaned[0],
        'unit' : dv_cleaned[1],
        'attr_id' : pd.to_numeric(dv['attr_id'])
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



##### now cleaning usda.csv

with open('usda.csv', 'rb') as f2:
    result = chardet.detect(f2.read())
usda = pd.read_csv('usda.csv', encoding=result['encoding']) # names=dv_names)

##### below are unused lines...
### selecting columns with str matching names
# dv_names = [ name.lower() for name in dv['name'].tolist() ] def isin_dv(usda_name):
#     for name in dv_names:
#         if name in usda_name.lower(): # str pattern matching. NOT finding in list
#             return True
#     return False
# 
# ### needed less strict criteria.
# def isin_dv2(usda_name):
#     usda_str = usda_name.lower()
#     for name in dv_names:
#         if 'vitamin' in name:
#             if name in usda_str:
#                 return True
#         else:
#             for word in name.split(' '):
#                 if word in usda_str:
#                     return True
#     return False
#         
# criterion = usda['name'].map(isin_dv2)
# usda = usda[criterion]
# 
##### dv handled manually since few and critical
# attr ids corresponding to dv
#with open('attr_ids.csv', 'rb') as f3: 
#    result = chardet.detect(f3.read())
# ids = pd.read_csv('attr_ids.csv', encoding=result['encoding'], dtype='int32')

# join dv and usda
print(dv, '\n\n\n', usda, '\n\n\n', dv.dtypes, '\n\n\n', usda.dtypes)
merged = pd.merge(dv, usda, on='attr_id')
print(merged)

