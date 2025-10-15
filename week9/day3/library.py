from book import Book # import Book class
# Library class to manage a collection of books

class Library: # Library class to manage a collection of books
    def __init__ (self):
        self.books = []  # list to store Book instances

    def add_book(self, book: Book):
        # avoid duplicate titles (case-insensitive)
        if self.find_book(book.title):
            print(f"'{book.title}' is already in the library.")
            return
        self.books.append(book)

    def list_books(self): # List all books with availability
        if not self.books: # No books
            print("No books available in the library.")
            return
        for book in self.books: # display each book
            status = "Available" if book.available else "Not Available"
            print(f" - '{book.title}' by {book.author} ({status})")

    def find_book(self, title): # Find book by title (case-insensitive)
        for book in self.books: # iterate through all books
            if book.title.lower() == title.lower():
                return book
        return None # not found

    def borrow_book(self, title): # Borrow a book by title
        book = self.find_book(title)
        if book: # found
            book.borrow()
        else: # not found
            print(f"Book '{title}' not found in the library.")

    def return_book(self, title): # Return a book by title
        book = self.find_book(title)
        if book: # found
            book.return_book()
        else: # not found
            print(f"Book '{title}' not found in the library.")
# book instances
book1 = Book("1984", "George Orwell")
book2 = Book("To Kill a Mockingbird", "Harper Lee")
book3 = Book("The Great Gatsby", "F. Scott Fitzgerald")
book4 = Book("Harry Potter and the Sorcerer's Stone", "J.K. Rowling")

library = Library()
library.add_book(book1)
library.add_book(book2)
library.add_book(book3)
library.add_book(book4)

def menu(): # Display menu options
    print("\nLibrary Menu:")
    print("1. List all books")
    print("2. Borrow a book")
    print("3. Return a book")
    print("4. Exit")

def main(): # Main program loop
    while True: # Keep running until user chooses to exit
        menu()
        choice = input("Choose an option (1-4): ").strip()
        if choice == "1":
            library.list_books()
        elif choice == "2":
            title = input("Enter the title of the book to borrow: ").strip()
            if not title:
                print("No title entered. Borrow canceled.")
            else:
                library.borrow_book(title)
        elif choice == "3":
            title = input("Enter the title of the book to return: ").strip()
            if not title:
                print("No title entered. Return canceled.")
            else:
                library.return_book(title)
        elif choice == "4":
            print("Exiting the library system.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
