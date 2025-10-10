# pizza project


from tabulate import tabulate # for formatting tables
import csv # for CSV handling
import sys # for command-line args

table = [] # to hold CSV data

if len(sys.argv) < 2: # check args
    sys.exit("Too few arguments.")
if len(sys.argv) > 2:
    sys.exit("Too many arguments.")

else: # exactly one argument
    csv_file = sys.argv[1] # get filename
    try: # read file
        if csv_file.endswith('.csv'):
            with open(csv_file) as file:
                reader = csv.reader(file)
                for row in reader: # read each row
                    table.append(row) # add to table
            # print formatted table
                print(tabulate(table, headers="firstrow", tablefmt="grid")) # grid format
        else: # not a CSV file
            sys.exit("Not a CSV file.")
    except FileNotFoundError: # file not found
        sys.exit("File does not exist.")
