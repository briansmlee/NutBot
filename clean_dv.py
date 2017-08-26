# script to clean usda and daily values csv files and join

import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import chardet

# determining file type due to encoding error
with open('daily_values.csv', 'rb') as f:
    result = chardet.detect(f.read())
    # print(result, '\n\n\n')

dv_names = ['name', 'daily_values', 'extra'] # specifying cols to handle inconsistent col nums
dv = pd.read_csv('daily_values.csv', encoding=result['encoding'], names=dv_names)
# print(dv)

dv = dv.drop(0) # remove first row due to repeated col names
# print('\n\n\n', dv) 
# clean unit by case
# use if unit is in parens

# usda = pd.DataFrame(usda['daily_values'].str.split(' ', 1).str,
#        columns = ['quantity', 'unit'])

dv_cleaned = dv['daily_values'].str.split(' ', 1, expand=True) # split dv into quantity, unit
# print(dv_cleaned)
dct = { 
        'name' : dv['name'],
        'quantity' : dv_cleaned[0],
        'unit' : dv_cleaned[1]
    }
        
dv = pd.DataFrame(dct)
print('\n\n\n', dv)

