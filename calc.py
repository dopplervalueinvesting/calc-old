#! /usr/bin/python

import os
import csv
from array import array

dir_analysis = os.getcwd()
os.chdir('..')
dir_doppler = os.getcwd()
dir_input = dir_doppler + '/input'
dir_output = dir_doppler + '/output'
os.chdir(dir_analysis)

def column (array_local, n_local):
    array_transpose = zip (*array_local)
    return array_transpose [n_local]

class CSVfile:
    def __init__ (self, filename):
        self.filename = filename

    def filearray (self):
        localarray = []
        with open (self.filename, 'rb') as f:
            reader = csv.reader (f, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            for row in reader:
                localarray.append (row)
        return localarray

class Stock:
    def __init__ (self, symbol):
        self.symbol = symbol

    def stockdata (self)
        file_stock = CSVfile (dir_input + '/' + stock_symbol + '.csv')
        array_stock = file_stock.filearray ()
        return array_stock

        

file_codes = CSVfile (dir_analysis + '/codes.csv')
array_codes = file_codes.filearray ()
cat_spec = column (array_codes, 1)[1:]
sign = column (array_codes, 2)[1:]
cat_gen = column (array_codes, 3)[1:]

file_companies = CSVfile (dir_input + '/company_list.csv')
array_companies = file_companies.filearray ()
list_symbols = column (array_companies, 0) [1:]
list_names = column (array_companies, 1) [1:]

stock_symbol = raw_input ('Enter the stock symbol of the company to analyze:\n')
i_symbol = list_symbols.index(stock_symbol)
stock_name = list_names [i_symbol]

# file_stock = CSVfile (dir_input + '/' + stock_symbol + '.csv')
# array_stock = file_stock.filearray ()
print array_stock

# if stock_symbol in list_symbols
#     imatch = 
#    stock_name = 
