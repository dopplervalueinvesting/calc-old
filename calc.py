#! /usr/bin/python

import os
import csv

dir_analysis = os.getcwd()
os.chdir('..')
dir_doppler = os.getcwd()
dir_input = dir_doppler + '/input'
dir_output = dir_doppler + '/output'
os.chdir(dir_analysis)

# Purpose: extract a given column from a 2-D list
# Input: 2-D data list
# Output: 1-D data list representing the (n_local+1) -th column of the input list
def column (list_local, n_local):
    list_transpose = zip (*list_local)
    return list_transpose [n_local]

# Purpose: extract a given column from a 2-D list but omit the top row
# Input: 2D data list
# Output: 1D data list representing the (n_local+1) -th column of the input list, minus the first entry
def column_data (list_local, n_local):
    list1 = column (list_local, n_local)
    list2 = list1 [1:]
    return list2

# Purpose: count the number of columns in a 2-D list    
def num_of_columns (list_local):
    list_transpose = zip (*list_local)
    n_local = len (list_transpose)
    return n_local

# Cuts off the first two entries of an list and then reverses it
# Used to process the financial numbers in the stock data
# The first column is the line item.  The second column is the code.
# The numbers to process are in the rest of the data.
# Input: 2-D data list
# Output: 1-D data list representing the (n_local+1) -th row of the input list
def row_rev (list_local, n_local):
    list1 = list_local [n_local] # (n_local+1) -th row
    list2 = list1 [2:]
    list3 = list2 [::-1] # reverses list
    return list3
    
# Converts a row of strings into floating point numbers
# Input: 2-D list of strings
# Output: 2-D list of floating point numbers
def string_to_float (list_local):
	# Row number = r + 1, range is r = 0 to r = last row number - 1
	# Column number = c + 1, range is c = 0 to c = last column - 1
    r_min = 0
    r_max = len (list_local) - 1
    c_min = 0
    c_max = num_of_columns (list_local) - 1
    list1 = []
    list2 = []
    for r in xrange (r_min, r_max):
        for c in xrange (c_min, c_max):
            print r, c
            item_string = list_local [r][c]
            item_no_commas = item_string.replace(',', '')
            try:
                element = float (item_no_commas)
            except:
                element = None
            list2.append (element)
        list1.append (list2)
    return list1

# This defines the class CSVfile (filename).
# Input: name of csv file
# Output: 2-D list fed by the input file
class CSVfile:
    def __init__ (self, filename):
        self.filename = filename

    def filelist (self):
        locallist = []
        with open (self.filename, 'rb') as f:
            reader = csv.reader (f, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            for row in reader:
                locallist.append (row)
        return locallist

# This defines the class Stock (symbol)
# Input: stock symbol
# Outputs: 2-D data list fed by the input file and 1-D data lists
class Stock:
    def __init__ (self, symbol):
        self.symbol = symbol

    # Purpose: reads the contents of the financial data file into a 2-D list
    # Input: stock file
    # Output: 2-D data list
    def data (self):
        file_stock = CSVfile (dir_input + '/' + self.symbol + '.csv')
        list_stock = file_stock.filelist ()
        return list_stock

    # Purpose: reads the contents of the company_list.csv file to 
    # find the name of a company given the ticker symbol
    # Input: stock file
    # Output: string
    def name (self):
        file_companies = CSVfile (dir_input + '/company_list.csv')
        list_companies = file_companies.filelist ()
        list_symbols = column_data (list_companies, 0)
        list_names = column_data (list_companies, 1)
        i_symbol = list_symbols.index(self.symbol)
        return list_names [i_symbol]
        
    # Purpose: extracts the title of each line item into a 1-D list
    # Input: 2-D data list from data function
    # Output: 1-D list of integers (first column, excluding the top row)
    def lineitem_titles (self):
        list1 = self.data ()
        list2 = column_data (list1, 0)
        return list2

    # Input: 2-D list from data function
    # Output: 2-D list (3 columns)
    # First column: specific codes
    # Second column: general codes
    # Third column: signs, +1 or -1
    def lineitem_codes (self):
        list1 = self.data ()
        spec_local = column_data (list1, 1) # First column of stock data
        finallist = []
        file_codes = CSVfile (dir_analysis + '/codes.csv')
        list_codefile = file_codes.filelist ()
        spec_codefile = column_data (list_codefile, 1)
        gen_codefile = column_data (list_codefile, 3)
        signs_codefile = column_data (list_codefile, 2)
        local_spec_lineitems = spec_local
        local_gen_lineitems = []
        local_signs_lineitems = []
        for item in local_spec_lineitems: # Go through the specific codes in the stock data
            try:
                i_spec = spec_codefile.index (item)
                local_gen_lineitems.append (gen_codefile [i_spec])
                local_signs_lineitems.append (signs_codefile [i_spec])
            except:
				local_gen_lineitems.append ('N/A')
				local_signs_lineitems.append ('0')
        finallist = zip (local_spec_lineitems, local_signs_lineitems, local_gen_lineitems)
        finallist = zip (finallist)
        return finallist

    # Input: 2-D list of strings and integers from lineitem_codes
    # Output: 1-D list
    def lineitem_spec (self):
        list1 = self.lineitem_codes ()
        locallist = column_data (column_data (list1, 0), 0)
        return locallist
    
    # Input: 2-D list of strings and integers from lineitem_codes
    # Output: 1-D list of numbers
    def lineitem_signs (self):
        list1 = self.lineitem_codes ()
        list2 = column_data (column_data (list1, 0), 1)
        list3 = string_to_float (list2)
        return list3
        
    # Input: 2-D list of strings and integers from lineitem_codes
    # Output: 1-D list    
    def lineitem_gen (self):
        list1 = self.lineitem_codes ()
        locallist = column_data (column_data (list1, 0), 2)
        return locallist
        
    # Purpose: extract the list of years
    # Input: 2-D data list from data function
    # Output: 1-D list of integers (top row, excluding the first two columns)
    # Note also the reversal, which puts the most recent year last in the sequence
    def years (self):
        list1 = self.data ()
        list2 = row_rev (list1, 0) # Removes the first two columns, then reverses
        return list2
        
    # Purpose: extract the split factor for each year
    # Input: 2-D data list from data function
    # Output: 1-D list of numbers (2nd row, excluding the first two columns)
    # Note also the reversal, which puts the most recent year last in the sequence
    def split_f (self):
        list1 = self.data ()
        list2 = row_rev (list1, 1) # Removes the first two columns, then reverses
        list3 = [float(i) for i in list2]
        return list3

    # Input: 2-D data list from data function
    # Output: 2-D list of numbers (excluding the top row and first two columns)
    # Note also the reversal, which puts the most recent year last in the sequence
    # Note that the strings are transformed into floating point numbers
    def lineitem_figures (self):
        list1 = self.data ()
        list3 = []
		# Row number = r + 1
		# First row: r = 0
		# Last row: r = total number of rows - 1
        r_min = 2 # top row = year, 2nd row = split factor
        r_max = len (list1) - 1
        for r in xrange (r_min, r_max):
            list2 = row_rev (list1, r) # Removes the first two columns, then reverses
            list3.append (list2)
        list4 = string_to_float (list3)
        return list4
                
    
        

stock_symbol = 'fast'
# stock_symbol = raw_input ('Enter the stock symbol of the company to analyze:\n')
mystock = Stock (stock_symbol)



mysigns = mystock.lineitem_signs ()

myfigures = mystock.lineitem_figures ()

mysplitf = mystock.split_f ()

# print myfigures




