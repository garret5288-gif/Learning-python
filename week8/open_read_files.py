# Example of reading from and writing to a file in Python

with open("newfile.txt", "w") as file: # open file for writing
    file.write("Hello, World!\n")
    file.write("This is a new file.\n")
    print("File written successfully.")

with open("newfile.txt", "r") as file: # open file for reading
    content = file.read()
    print("File content:")
    print(content)