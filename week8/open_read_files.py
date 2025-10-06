# Example of reading from and writing to a file in Python

FILE_PATH = "newfile.txt"

with open(FILE_PATH, "r") as file:  # open file for reading
    content = file.read()
    print("File content:")
    print(content)

with open(FILE_PATH, "a") as file:  # open file for appending
    file.write("\nAppended line.")
    print("Appended a new line to the file.")
    print("Updated file content:")
    with open(FILE_PATH, "r") as f:  # re-open for reading
        print(f.read())