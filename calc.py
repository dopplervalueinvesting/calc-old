#! /usr/bin/python

import os
import csv
import numpy

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
# Input: 2-D data list
# Output: 1-D data list representing the (n_local+1) -th column of the input list, minus the first entry
def column_data (list_local, n_local):
    list1 = column (list_local, n_local)
    list2 = list1 [1:]
    return list2

# Purpose: count the number of columns in a 2-D list
# Input: 2-D data list
# Output: integer representing the number of columns of the 2-D list
def num_of_columns (list_local):
    list_transpose = zip (*list_local)
    n_local = len (list_transpose)
    return n_local

# Cuts off the first two entries of a list and then reverses it
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
# Input: 1-D list of strings
# Output: 1-D list of floating point numbers
def string_to_float (list_local):
    list1 = []
    for item in list_local:
        item1 = item
        item2 = item1.replace (',', '')
        try:
            item3 = float (item2)
        except:
            item3 = None
        list1.append (item3)
    return list1
    
# Converts a row of strings into integers
# Input: 1-D list of strings
# Output: 1-D list of floating point numbers
def string_to_int (list_local):
    list1 = []
    for item in list_local:
        item1 = item
        item2 = item1.replace (',', '')
        try:
            item3 = int (item2)
        except:
            item3 = None
        list1.append (item3)
    return list1
    
# Finds the average in a list of numbers
# Input: 1-D list of floating point numbers
# Output: floating point number
def mean (list_local):
    try:
        total = float (sum (list_local))
        n = len (list_local)
        x = float (total/n)
    except:
        x = None
    return x

# Finds the n_local-element moving average in a list of numbers
# Input: 1-D list of floating point numbers
# Output: 1-D list of floating point numbers
def moving_average (list_local, n_local):
    list1 = list_local
    list2 = []
    n_cols = len (list1)
    c_min = 0
    c_max = n_cols - 1
    c = c_min
    x_min = 0
    x_max = n_local - 1
    while c <= c_max:
        list3 = []
        x = x_min
        while x <= x_max:
            if c - x < 0:
                element = None
            else:
                element = list1 [c - x]
            list3.append (element)
            x = x + 1
        ave_moving = mean (list3)
        list2.append (ave_moving)
        c = c + 1
    return list2
        	
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
    def __init__ (self, symbol, n_smooth, price):
        self.symbol = symbol
        self.n_smooth = n_smooth
        self.price = price
    
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
        list2 = column_data (list1, 0) # Excludes the top row of the stock data file
        list3 = list2 [2:] # Excludes the next 2 rows of the stock data file
        return list3

    # Purpose: extracts the specific category, general category, and sign (+/-) for each line item
    # Input: 2-D list from data function
    # Output: 2-D list (3 columns)
    # First column: specific codes
    # Second column: general codes
    # Third column: signs, +1 or -1
    def lineitem_codes (self):
        list1 = self.data ()
        spec_local = column_data (list1, 1) # First column of stock data, excludes the top row
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

    # Purpose: obtain the specific category for each line item
    # Input: 2-D list of strings and integers from lineitem_codes
    # Output: 1-D list
    def lineitem_spec (self):
        list1 = self.lineitem_codes () # Excludes the top row
        locallist = column_data (column_data (list1, 0), 0) # Excludes the next two rows
        return locallist
    
    # Purpose: obtain the +/- sign for each line item
    # Input: 2-D list of strings and integers from lineitem_codes
    # Output: 1-D array of numbers
    def lineitem_signs (self):
        list1 = self.lineitem_codes () # Excludes the top row
        list2 = column_data (column_data (list1, 0), 1) # Excludes the next two rows
        list3 = string_to_int (list2)
        return list3
        
    # Purpose: obtain the general category for each line item
    # Input: 2-D list of strings and integers from lineitem_codes
    # Output: 1-D list    
    def lineitem_gen (self):
        list1 = self.lineitem_codes () # Excludes the top row
        locallist = column_data (column_data (list1, 0), 2) # Excludes the next two rows
        return locallist
        
    # Purpose: extract the list of years
    # Input: 2-D data list from data function
    # Output: 1-D list (top row, excluding the first two columns)
    # Note also the reversal, which puts the most recent year last in the sequence
    def years (self):
        list1 = self.data ()
        list2 = row_rev (list1, 0) # Removes the first two columns, then reverses
        return list2
        
    # Purpose: extract the split factor for each year
    # Input: 2-D data list from data function
    # Output: 1-D array of numbers (2nd row, excluding the first two columns)
    # Note also the reversal, which puts the most recent year last in the sequence
    def split_f (self):
        list1 = self.data ()
        list2 = row_rev (list1, 1) # Removes the first two columns, then reverses
        list3 = string_to_float (list2)
        return list3
        
    # Purpose: extract the split factor for each year
    # Input: 2-D data list from data function
    # Output: 1-D list of numbers (3rd row, excluding the first two columns)
    # Note also the reversal, which puts the most recent year last in the sequence
    def unit_plus(self):
        list1 = self.data ()
        list2 = row_rev (list1, 2) # Removes the first two columns, then reverses
        list3 = string_to_float (list2)
        return list3
                
    # Purpose: extract the split factor for each year
    # Input: 2-D data list from data function
    # Output: 1-D list of numbers (4th row, excluding the first two columns) OR
    # a 1-D list of zeros
    # Note also the reversal, which puts the most recent year last in the sequence
    def unit_minus (self):
        list1 = self.data ()
        list2 = row_rev (list1, 3) # Removes the first two columns, then reverses
        if list1 [3][1] == 'un-':
            list3 = string_to_float (list2)
        else:
            list3 = [0 for i in list2]
        return list3

    # Purpose: obtain the number of line items
    # Input: 1-D data list from lineitem_figures function
    # Output: integer (number of rows in lineitem_figures)
    def num_lineitems (self):
		list1 = self.lineitem_spec ()
		local_num = len (list1)
		return local_num
	
	# Purpose: obtain the number of years of data
	# Input: 1-D data list from years function
    # Output: integer (number of rows in lineitem_figures)
    def num_years (self):
		list1 = self.years ()
		local_num = len (list1)
		return local_num

    # Purpose: obtain the financial figures in numbers to be used for computation
    # Input: 2-D data list from data function
    # Output: 2-D list of numbers (excluding the top row and first two columns)
    # Note also the reversal, which puts the most recent year last in the sequence
    # Note that the strings are transformed into floating point numbers
    def lineitem_figures (self):
        list1 = self.data ()
        # Row number = r + 1
		# First row: r = 0
		# Last row: r = total number of rows - 1
        r_max_data = len (list1) -1
        r_min_data = 3 # top row = year, 2nd row = split factor, 3rd row = unit (plus)
        list2 = []
        for r_data in xrange (r_min_data, r_max_data):
            line1 = row_rev(list1, r_data) # Reverses, cuts off first two columns
            list2.append (line1)
        # list2 = data minus first two columns and first three rows
        list3 = []
        for line in list2:
            line1 = line
            line2 = string_to_float (line1)
            list3.append (line2)
        # list3 = list2 converted to floating point numbers
        return list3
        
    # Obtain the list of line items for a given combination of general category and sign
    # Input: 1-D data lists from lineitem_gen function and lineitem_signs
    # Output: 1-D list of line numbers
    def lineitem_index (self, gen_seek, sign_seek):
        list1 = self.lineitem_gen ()
        list2 = self.lineitem_signs ()
        list3 = []
        # Row number = r + 1
		# First row: r = 0
		# Last row: r = total number of rows - 1
        r_max_data = len (list1) -1
        r_min_data = 0
        for r in xrange (r_min_data, r_max_data):
            if list1 [r] == gen_seek:
                if list2 [r] == sign_seek:
                    list3.append (r)
        return list3
        
    # Obtain the list of titles for the line items of a given general category and sign
    # Inputs: 1-D lists
    # Output: 1-D list
    def lineitem_cat_titles (self, gen_seek, sign_seek):
        list1 = self.lineitem_index (gen_seek, sign_seek)
        list2 = self.lineitem_titles ()
        list3 = []
        for item in list1:
            list3.append (list2 [item])
        return list3

    # Obtain the list of specific categories for the line items of a given general category and sign
    # Inputs: 1-D lists
    # Output: 1-D list	
    def lineitem_cat_spec (self, gen_seek, sign_seek):
        list1 = self.lineitem_index (gen_seek, sign_seek)
        list2 = self.lineitem_spec ()
        list3 = []
        for item in list1:
            list3.append (list2 [item])
        return list3
        
    # Obtain the figures for the line items of a given general category and sign
    # Inputs: 1-D lists
    # Output: 2-D list
    def lineitem_cat_figures (self, gen_seek, sign_seek):
        list1 = self.lineitem_index (gen_seek, sign_seek)
        list2 = self.lineitem_figures ()
        list3 = []
        for item in list1:
            list3.append (list2 [item])
        return list3
    
    # Obtain the total figures for a given general category and sign
    # NOTE: These figures are in NOMINAL units, not dollars.
    # Inputs: 1-D lists, 2-D list
    # Output: 1-D list
    def lineitem_cat_total (self, gen_seek, sign_seek):
        list1 = self.lineitem_cat_figures (gen_seek, sign_seek)
        list2 = []
        n_rows = len (list1)
        n_cols = num_of_columns (list1)
        r_min = 0
        r_max = n_rows - 1
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            local_total = 0
            r = r_min
            while r <= r_max:
                try:
                    local_total = local_total + list1 [r][c]
                except:
                    local_total = None
                r = r + 1
            list2.append (local_total)
            c = c + 1
        return list2
        
    def liqplus_titles (self):
        list1 = self.lineitem_cat_titles ('liq', 1)
        return list1
        
    def liqplus_spec (self):
        list1 = self.lineitem_cat_spec ('liq', 1)
        return list1
    
    def liqplus (self):
        list1 = self.lineitem_cat_total ('liq', 1)
        return list1
    
    def liqminus_titles (self):
        list1 = self.lineitem_cat_titles ('liq', -1)
        return list1
        
    def liqminus_spec (self):
        list1 = self.lineitem_cat_spec ('liq', -1)
        return list1
    
    def liqminus (self):
        list1 = self.lineitem_cat_total ('liq', -1)
        return list1
    
    # Liquid assets ($)
    def dollars_liq (self):
        list_unplus  = self.unit_plus ()
        list_unminus = self.unit_minus ()
        list_liqplus = self.liqplus ()
        list_liqminus = self.liqminus ()
        list1 = []
        n_cols = len (list_liqplus)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                dollars = list_unplus [c] * list_liqplus [c] - list_unminus [c] * list_liqminus [c]
            except:
                try:
                    dollars = list_unplus [c] * list_liqplus [c]
                except:
                    dollars = None
            list1.append (dollars)
            c = c + 1
        return list1
        
    def liabplus_titles (self):
        list1 = self.lineitem_cat_titles ('liab', 1)
        return list1
        
    def liabplus_spec (self):
        list1 = self.lineitem_cat_spec ('liab', 1)
        return list1
    
    def liabplus (self):
        list1 = self.lineitem_cat_total ('liab', 1)
        return list1
    
    def liabminus_titles (self):
        list1 = self.lineitem_cat_titles ('liab', -1)
        return list1
        
    def liabminus_spec (self):
        list1 = self.lineitem_cat_spec ('liab', -1)
        return list1
    
    def liabminus (self):
        list1 = self.lineitem_cat_total ('liab', -1)
        return list1
        
    # Nonconvertible liabilities ($)        
    def dollars_liab (self):
        list_unplus  = self.unit_plus ()
        list_unminus = self.unit_minus ()
        list_quantplus = self.liabplus ()
        list_quantminus = self.liabminus ()
        list1 = []
        n_cols = len (list_quantplus)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                dollars = list_unplus [c] * list_quantplus [c] - list_unminus [c] * list_quantminus [c]
            except:
                try:
                    dollars = list_unplus [c] * list_quantplus [c]
                except:
                    dollars = None
            list1.append (dollars)
            c = c + 1
        return list1
        
    # Net liquid assets, convertibles as shares ($)
    def dollars_netliq_nc (self):
        list_liq = self.dollars_liq ()
        list_liab = self.dollars_liab ()
        list1 = []
        n_cols = len (list_liq)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                dollars = list_liq [c] - list_liab [c]
            except:
                dollars = None
            list1.append (dollars)
            c = c + 1
        return list1

    def liabc_titles (self):
        list1 = self.lineitem_cat_titles ('liabc', 1)
        return list1
        
    def liabc_spec (self):
        list1 = self.lineitem_cat_spec ('liabc', 1)
        return list1
    
    def liabc (self):
        list1 = self.lineitem_cat_total ('liabc', 1)
        return list1
    
    # Convertible liabilities ($)
    def dollars_liabc (self):
        list_quantplus = self.liabc ()
        list_unplus = self.unit_plus ()
        list1 = []
        n_cols = len (list_unplus)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                dollars = list_unplus [c] * list_quantplus [c]
            except:
                dollars = 0    
            list1.append (dollars)
            c = c + 1
        return list1
        
    # Net liquidity, convertibles as debt ($)
    def dollars_netliq_conv (self):
        list_netliq = self.dollars_netliq_nc ()
        list_liabc = self.dollars_liabc ()
        list1 = []
        n_cols = len (list_netliq)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                dollars = list_netliq [c] - list_liabc [c]
            except:
                dollars = None
            list1.append (dollars)
            c = c + 1
        return list1
        
    def shares_titles (self):
        list1 = self.lineitem_cat_titles ('shares', 1)
        return list1
        
    def shares_spec (self):
        list1 = self.lineitem_cat_spec ('shares', 1)
        return list1
    
    def shares_nc (self):
        list1 = self.lineitem_cat_total ('shares', 1)
        return list1

    def shares_conv_titles (self):
        list1 = self.lineitem_cat_titles ('sharesc', 1)
        return list1
        
    def shares_conv_spec (self):
        list1 = self.lineitem_cat_spec ('sharesc', 1)
        return list1
        
    # Convertible shares, 0 if not listed
    def shares_conv (self):
        list1 = self.lineitem_cat_total ('sharesc', 1)
        list2 = []
        n_cols = len (list1)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            conv = list1 [c]
            if (conv == None):
                conv = 0
            list2.append (conv)
            c = c + 1
        return list2
        
    # Total shares, split adjusted, convertibles as debt
    def shares_adj_nc (self):
        list1 = self.shares_nc ()
        list2 = self.split_f ()
        list3 = []
        n_cols = len (list1)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                local_shares = list1 [c] * list2 [c]
            except:
                local_shares = None
            list3.append (local_shares)
            c = c + 1
        return list3
        
    # Total shares, split adjusted, convertibles as shares
    def shares_adj_conv (self):
        list1 = self.shares_nc ()
        list2 = self.shares_conv ()
        list3 = self.split_f ()
        list4 = []
        n_cols = len (list1)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                local_shares = (list1 [c] + list2 [c]) * list3 [c]
            except:
                try:
                    local_shares = (list1 [c]) * list3 [c]
                except:
                    local_shares = None
            list4.append (local_shares)
            c = c + 1
        return list4
		
    def ppecplus_titles (self):
        list1 = self.lineitem_cat_titles ('ppec', 1)
        return list1
        
    def ppecplus_spec (self):
        list1 = self.lineitem_cat_spec ('ppec', 1)
        return list1
    
    def ppecplus (self):
        list1 = self.lineitem_cat_total ('ppec', 1)
        return list1
    
    def ppecminus_titles (self):
        list1 = self.lineitem_cat_titles ('ppec', -1)
        return list1
        
    def ppecminus_spec (self):
        list1 = self.lineitem_cat_spec ('ppec', -1)
        return list1
    
    def ppecminus (self):
        list1 = self.lineitem_cat_total ('ppec', -1)
        return list1

    # Plant/property/equipment capital ($)
    def dollars_ppec (self):
        list_unplus  = self.unit_plus ()
        list_unminus = self.unit_minus ()
        list_quantplus = self.ppecplus ()
        list_quantminus = self.ppecminus ()
        list1 = []
        n_cols = len (list_quantplus)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                dollars = list_unplus [c] * list_quantplus [c] - list_unminus [c] * list_quantminus [c]
            except:
                try:
                    dollars = list_unplus [c] * list_quantplus [c]
                except:
                    dollars = None
            list1.append (dollars)
            c = c + 1
        return list1
        
    def salesplus_titles (self):
        list1 = self.lineitem_cat_titles ('rev', 1)
        return list1
        
    def salesplus_spec (self):
        list1 = self.lineitem_cat_spec ('rev', 1)
        return list1
    
    def salesplus (self):
        list1 = self.lineitem_cat_total ('rev', 1)
        return list1
    
    def salesminus_titles (self):
        list1 = self.lineitem_cat_titles ('rev', -1)
        return list1
        
    def salesminus_spec (self):
        list1 = self.lineitem_cat_spec ('rev', -1)
        return list1
    
    def salesminus (self):
        list1 = self.lineitem_cat_total ('rev', -1)
        return list1
        
    # Net revenues ($)
    def dollars_sales (self):
        list_unplus  = self.unit_plus ()
        list_unminus = self.unit_minus ()
        list_quantplus = self.salesplus ()
        list_quantminus = self.salesminus ()
        list1 = []
        n_cols = len (list_quantplus)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                dollars = list_unplus [c] * list_quantplus [c] - list_unminus [c] * list_quantminus [c]
            except:
                try:
                    dollars = list_unplus [c] * list_quantplus [c]
                except:
                    dollars = None
            list1.append (dollars)
            c = c + 1
        return list1

    def exp_plus_titles (self):
        list1 = self.lineitem_cat_titles ('exp', 1)
        return list1
        
    def exp_plus_spec (self):
        list1 = self.lineitem_cat_spec ('exp', 1)
        return list1
    
    def exp_plus (self):
        list1 = self.lineitem_cat_total ('exp', 1)
        return list1
    
    def exp_minus_titles (self):
        list1 = self.lineitem_cat_titles ('exp', -1)
        return list1
        
    def exp_minus_spec (self):
        list1 = self.lineitem_cat_spec ('exp', -1)
        return list1
    
    def exp_minus (self):
        list1 = self.lineitem_cat_total ('exp', -1)
        return list1

    # Expenses ($)
    def dollars_exp (self):
        list_unplus  = self.unit_plus ()
        list_unminus = self.unit_minus ()
        list_quantplus = self.exp_plus ()
        list_quantminus = self.exp_minus ()
        list1 = []
        n_cols = len (list_quantplus)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                dollars = list_unplus [c] * list_quantplus [c] - list_unminus [c] * list_quantminus [c]
            except:
                try:
                    dollars = list_unplus [c] * list_quantplus [c]
                except:
                    dollars = None
            list1.append (dollars)
            c = c + 1
        return list1

    def cfadj_plus_titles (self):
        list1 = self.lineitem_cat_titles ('adj', 1)
        return list1
        
    def cfadj_plus_spec (self):
        list1 = self.lineitem_cat_spec ('adj', 1)
        return list1
    
    def cfadj_plus (self):
        list1 = self.lineitem_cat_total ('adj', 1)
        return list1
    
    def cfadj_minus_titles (self):
        list1 = self.lineitem_cat_titles ('adj', -1)
        return list1
        
    def cfadj_minus_spec (self):
        list1 = self.lineitem_cat_spec ('adj', -1)
        return list1
    
    def cfadj_minus (self):
        list1 = self.lineitem_cat_total ('adj', -1)
        return list1

    # Cash flow adjustments ($)
    def dollars_cfadj (self):
        list_unplus  = self.unit_plus ()
        list_unminus = self.unit_minus ()
        list_quantplus = self.cfadj_plus ()
        list_quantminus = self.cfadj_minus ()
        list1 = []
        n_cols = len (list_quantplus)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                dollars = list_unplus [c] * list_quantplus [c] - list_unminus [c] * list_quantminus [c]
            except:
                try:
                    dollars = list_unplus [c] * list_quantplus [c]
                except:
                    dollars = None
            list1.append (dollars)
            c = c + 1
        return list1

    # Cash flow ($)
    def dollars_cf (self):
        list1 = self.dollars_sales ()
        list2 = self.dollars_exp ()
        list3 = self.dollars_cfadj ()
        list4 = []
        n_cols = len (list1)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                dollars = list1[c] - list2 [c] + list3 [c]
            except:
                dollars = None
            list4.append (dollars)
            c = c + 1
        return list4

    # Normalized capital spending ($)
    def dollars_cap (self):
        list1 = self.dollars_ppec ()
        list2 = []
        n_cols = len (list1)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                if c - 1 < 0:
                    dollars = None
                else:
                    dollars = .1 * list1 [c-1]
            except:
                dollars = None
            list2.append (dollars)
            c = c + 1
        return list2

    # Free cash flow, unsmoothed ($)
    def dollars_fcf (self):
        list1 = self.dollars_cf ()
        list2 = self.dollars_cap ()
        list3 = []
        n_cols = len (list1)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                dollars = list1 [c] - list2 [c]
            except:
                dollars = None
            list3.append (dollars)
            c = c + 1
        return list3

    # Doppler ROE, return on PPE
    # (free cash flow in year y divided by plant/property/equipment in year y-1)
    def return_ppe (self):
        list1 = self.dollars_fcf ()
        list2 = self.dollars_ppec ()
        list3 = []
        n_cols = len (list1)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                if c - 1 < 0:
                    dollars = None
                else:
                    dollars = list1[c] / list2[c-1]
            except:
                dollars = None
            list3.append (dollars)
            c = c + 1
        return list3

    # Net liquid assets, convertible = debt, $ per share
    def psh_netliq_cdebt (self):
        list1 = self.dollars_netliq_conv ()
        list2 = self.shares_adj_nc ()
        list3 = []
        n_cols = len (list1)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                psh = list1[c] / list2[c]
            except:
                psh = None
            list3.append (psh)
            c = c + 1
        return list3

    # Net liquid assets, convertible = shares, $ per share
    def psh_netliq_cshares (self):
        list1 = self.dollars_netliq_nc ()
        list2 = self.shares_adj_conv ()
        list3 = []
        n_cols = len (list1)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                psh = list1[c] / list2[c]
            except:
                psh = None
            list3.append (psh)
            c = c + 1
        return list3
        
    def psh_ppec_cdebt (self):
        list1 = self.dollars_ppec ()
        list2 = self.shares_adj_nc ()
        list3 = []
        n_cols = len (list1)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                psh = list1[c] / list2[c]
            except:
                psh = None
            list3.append (psh)
            c = c + 1
        return list3
        
    def psh_ppec_cshares (self):
        list1 = self.dollars_ppec ()
        list2 = self.shares_adj_conv ()
        list3 = []
        n_cols = len (list1)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                psh = list1[c] / list2[c]
            except:
                psh = None
            list3.append (psh)
            c = c + 1
        return list3

    def return_ppe_ave (self):
        list1 = self.return_ppe ()
        n = n_ave
        list2 = moving_average (list1, n)
        return list2
        
    def psh_fcf_smooth_cdebt (self):
        list1 = self.return_ppe_ave ()
        list2 = self.psh_ppec_cdebt ()
        list3 = []
        n_cols = len (list1)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                if c-1<0:
                    psh = None
                else:
                    psh = list1[c] * list2[c-1]
            except:
                psh = None
            list3.append (psh)
            c = c + 1
        return list3
        
    def psh_fcf_smooth_cshares (self):
        list1 = self.return_ppe_ave ()
        list2 = self.psh_ppec_cshares ()
        list3 = []
        n_cols = len (list1)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                if c-1<0:
                    psh = None
                else:
                    psh = list1[c] * list2[c-1]
            except:
                psh = None
            list3.append (psh)
            c = c + 1
        return list3

    def psh_intrinsic_cdebt (self):
        list1 = self.psh_netliq_cdebt ()
        list2 = self.psh_ppec_cdebt ()
        list3 = self.return_ppe ()
        list4 = []
        n_cols = len (list1)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                if c-1<0:
                    psh = None
                else:
                    psh = list1[c-1] + 10 * list2[c-1] * list3 [c-1]
            except:
                psh = None
            list4.append (psh)
            c = c + 1
        return list4
        
    def psh_intrinsic_cshares (self):
        list1 = self.psh_netliq_cshares ()
        list2 = self.psh_ppec_cshares ()
        list3 = self.return_ppe ()
        list4 = []
        n_cols = len (list1)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                if c-1<0:
                    psh = None
                else:
                    psh = list1[c-1] + 10 * list2[c-1] * list3 [c-1]
            except:
                psh = None
            list4.append (psh)
            c = c + 1
        return list4

    def psh_bargain_cdebt (self):
        list1 = self.psh_netliq_cdebt ()
        list2 = self.psh_ppec_cdebt ()
        list3 = self.return_ppe ()
        list4 = []
        n_cols = len (list1)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                if c-1<0:
                    psh = None
                else:
                    psh = list1[c-1] + (10/1.5) * list2[c-1] * list3 [c-1]
            except:
                psh = None
            list4.append (psh)
            c = c + 1
        return list4

    def psh_bargain_cshares (self):
        list1 = self.psh_netliq_cshares ()
        list2 = self.psh_ppec_cshares ()
        list3 = self.return_ppe ()
        list4 = []
        n_cols = len (list1)
        c_min = 0
        c_max = n_cols - 1
        c = c_min
        while c <= c_max:
            try:
                if c-1<0:
                    psh = None
                else:
                    psh = list1[c-1] + (10/1.5) * list2[c-1] * list3 [c-1]
            except:
                psh = None
            list4.append (psh)
            c = c + 1
        return list4

    def doppler_pb (self):
        p = price
        list1 = self.psh_intrinsic_cdebt ()
        list2 = self.psh_intrinsic_cshares ()
        bv1 = list1 [-1]
        bv2 = list2 [-1]
        bv = min (bv1, bv2)
        pb = p/bv
        return pb
    
    def doppler_pe (self):
        p = price
        list1 = self.psh_fcf_smooth_cdebt ()
        list2 = self.psh_fcf_smooth_cshares ()
        list3 = self.psh_netliq_cdebt ()
        list4 = self.psh_netliq_cshares ()
        e1 = list1 [-1]
        e2 = list2 [-1]
        p_adj_1 = p - list3 [-1]
        p_adj_2 = p - list4 [-1]
        pe1 = p_adj_1 / e1
        pe2 = p_adj_2 / e2
        pe = max (pe1, pe2)
        return pe
    
    def doppler_eyld (self):
        p = price
        list1 = self.psh_fcf_smooth_cdebt ()
        list2 = self.psh_fcf_smooth_cshares ()
        list3 = self.psh_netliq_cdebt ()
        list4 = self.psh_netliq_cshares ()
        e1 = list1 [-1]
        e2 = list2 [-1]
        p_adj_1 = p - list3 [-1]
        p_adj_2 = p - list4 [-1]
        yld1 = e1 / p_adj_1
        yld2 = e2 / p_adj_2
        yld = min (yld1, yld2)
        return yld

stock_symbol = 'fast'
# stock_symbol = raw_input ('Enter the stock symbol of the company to analyze:\n')
n_ave = int (raw_input ('Enter the number of years of data to use for smoothing:\n'))
price = float (raw_input ('Enter the current stock price:\n'))
mystock = Stock (stock_symbol, n_ave, price)


print '\n\n'
myliqplusspec = mystock.liqplus_spec ()
myliqplustitles = mystock.liqplus_titles ()
myliqplus = mystock.liqplus ()
print myliqplusspec, myliqplustitles, myliqplus
myliqminusspec = mystock.liqminus_spec ()
myliqminustitles = mystock.liqminus_titles ()
myliqminus = mystock.liqminus ()

myliqdollars = mystock.dollars_liq ()
print myliqdollars
myliabdollars = mystock.dollars_liab ()
print myliabdollars
mynetliq = mystock.dollars_netliq_nc ()
print mynetliq
print '\n\n'
myliabc = mystock.dollars_liabc ()
print myliabc
mynetliqc = mystock.dollars_netliq_conv ()
print mynetliqc
myshares = mystock.shares_nc ()
print myshares
myshares = mystock.shares_adj_nc ()
print myshares
myshares = mystock.shares_adj_conv ()
print myshares
myppec = mystock.dollars_ppec ()
print myppec
print '\n\n'
mysales = mystock.dollars_sales ()
print mysales
print '\n\n'
mycashflow = mystock.dollars_cf ()
print mycashflow
mycap = mystock.dollars_cap ()
print mycap
myfcf = mystock.dollars_fcf ()
print myfcf
myroe = mystock.return_ppe ()
print myroe
my_psh_netliq = mystock.psh_netliq_cdebt ()
print my_psh_netliq
my_psh_netliq = mystock.psh_netliq_cshares ()
print my_psh_netliq
my_psh_ppec = mystock.psh_ppec_cdebt ()
print my_psh_ppec
my_psh_ppec = mystock.psh_ppec_cshares ()
print my_psh_ppec
myppeave = mystock.return_ppe_ave ()
print myppeave

myfcfsmooth = mystock.psh_fcf_smooth_cdebt ()
print myfcfsmooth

myfcfsmooth = mystock.psh_fcf_smooth_cshares ()
print myfcfsmooth

myintrinsic = mystock.psh_intrinsic_cdebt ()
print myintrinsic
myintrinsic = mystock.psh_intrinsic_cshares ()
print myintrinsic
mybargain = mystock.psh_bargain_cdebt()
print mybargain
mybargain = mystock.psh_bargain_cshares ()
print mybargain

my_pb = mystock.doppler_pb ()
my_pe = mystock.doppler_pe ()
my_eyld = mystock.doppler_eyld ()
print my_pb, my_pe, my_eyld
