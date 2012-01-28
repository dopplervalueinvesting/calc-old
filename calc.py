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

# Input: 2-D data array
# Output: 1-D data array representing the (n_local+1) -th column of the input array
def column (array_local, n_local):
    array_transpose = zip (*array_local)
    return array_transpose [n_local]

# Input: 2D data array
# Output: 1D data array representing the (n_local+1) -th column of the input array, minus the first entry
def column_data (array_local, n_local):
    array1 = column (array_local, n_local)
    array2 = array1 [1:]
    return array2

# Cuts off the first two entries of an array and then reverses it
# Used to process the financial numbers in the stock data
# The first column is the line item.  The second column is the code.
# The numbers to process are in the rest of the data.
# Input: 2-D data array
# Output: 1-D data array representing the (n_local+1) -th row of the input array
def row_rev (array_local, n_local):
    array1 = array_local [n_local] # (n_local+1) -th row
    array2 = array1 [2:]
    array3 = array2 [::-1] # reverses array
    return array3

# This defines the class CSVfile (filename).
# Input: name of csv file
# Output: 2-D array fed by the input file
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

# This defines the class Stock (symbol)
# Input: stock symbol
# Outputs: 2-D data array fed by the input file and 1-D data arrays
class Stock:
    def __init__ (self, symbol):
        self.symbol = symbol

    # Output: 2-D data array
    def data (self):
        file_stock = CSVfile (dir_input + '/' + self.symbol + '.csv')
        array_stock = file_stock.filearray ()
        return array_stock

    # Output: string
    def name (self):
        file_companies = CSVfile (dir_input + '/company_list.csv')
        array_companies = file_companies.filearray ()
        list_symbols = column_data (array_companies, 0)
        list_names = column_data (array_companies, 1)
        i_symbol = list_symbols.index(self.symbol)
        return list_names [i_symbol]

    # Output: 1-D array of integers (top row, excluding the first two columns)
    def years (self):
        array1 = self.data ()
        array2 = row_rev (array1, 0)
        return array2

    # Output: 1-D array of integers (first column, excluding the top row)
    def lineitem_titles (self):
        array1 = self.data ()
        array2 = column_data (array1, 0)
        return array2

    # Output: 2D array of integers
    # First column: specific codes
    # Second column: general codes
    # Third column: signs, +1 or -1
    def lineitem_codes (self):
        array1 = self.data ()
        spec_local = column_data (array1, 1) # First column of stock data
        finalarray = []
        file_codes = CSVfile (dir_analysis + '/codes.csv')
        array_codefile = file_codes.filearray ()
        spec_codefile = column_data (array_codefile, 1)
        gen_codefile = column_data (array_codefile, 3)
        signs_codefile = column_data (array_codefile, 2)
        r = 0
        for item in spec_local: # Go through the specific codes in the stock data
            i_spec = spec_codefile.index (item)
            gen_local = gen_codefile [i_spec]
            signs_local = signs_codefile [i_spec]
            finalarray [r][0] = item
            finalarray [r][1] = signs_local
            finalarray [r][2] = gen_local
            r = r + 1
        return finalarray


        



# stock_symbol = raw_input ('Enter the stock symbol of the company to analyze:\n')
stock_symbol = 'fast'
mystock = Stock (stock_symbol)
# print mystock.data()
print mystock.name()
print mystock.years()
# myyears= mystock.years()
# print myyears [0]
print mystock.lineitem_titles()
print mystock.lineitem_codes()


