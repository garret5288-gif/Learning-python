# book class
# Represents a book in the library

class Book: # Book class to represent a book
    def __init__ (self, title, author, available=True):
        self.title = title
        self.author = author
        self.available = available

    def borrow(self): # Borrow the book if available
        if self.available:
            self.available = False # mark as not available
            print(f"You have borrowed '{self.title}'.")
        else: # not available
            print(f"Sorry, '{self.title}' is currently unavailable.")

    def return_book(self): # Return the book
        if not self.available:
            self.available = True # mark as available
            print(f"You have returned '{self.title}'.")
        else: # not borrowed
            print(f"'{self.title}' was not borrowed.")