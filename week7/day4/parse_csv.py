import csv
# Read and parse the CSV file into a list of dictionaries
file_path = "/Users/garretadkins/Documents/GitHub/Learning-python/Learning-python/week7/day4/contact.txt"

contacts = [] # List to hold contact dictionaries
with open(file_path, newline='') as csvfile: # Open the CSV file
    reader = csv.DictReader(csvfile) # Create a DictReader
    for row in reader: # Iterate over each row
        contacts.append(dict(row)) # Convert OrderedDict to dict and add to list

# Print all contacts as dictionaries
for contact in contacts: 
    print(contact)