# script to clean usda and daily values csv files and join

import pandas as pd
import csv
import matplotlib.pyplot as plt
import chardet

# determining file type due to encoding error
with open('daily_values.csv', 'rb') as f:
    result = chardet.detect(f.read())
    # print(result, '\n\n\n')

usda_names = ['name', 'daily_values', 'extra'] # specifying to handle inconsistent col nums
usda = pd.read_csv('daily_values.csv', names=usda_names, encoding=result['encoding'])
print(usda)


