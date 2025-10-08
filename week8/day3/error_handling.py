# error_handling
# Demonstrate basic error handling in Python

try: # Attempt to open a non-existent file
    with open("non_existent_file.txt", "r") as file:
        content = file.read()
        print(content)
except FileNotFoundError: # Handle file not found error
    print("Error: The file was not found.")
except IOError: # Handle I/O errors
    print("Error: An I/O error occurred.")
except Exception as e: # Handle any other exceptions
    print(f"An unexpected error occurred: {e}")
else: # No exceptions occurred
    print("File read successfully.")
finally: # Always execute this block
    print("Execution completed.")