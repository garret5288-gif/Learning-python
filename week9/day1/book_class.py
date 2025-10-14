# Book class definition and usage

class Book: # Define a Book class
    def __init__(self, title, author, year): # Constructor with title, author, year
        self.title = title
        self.author = author
        self.year = year

    def get_summary(self): # Method to get book summary
        return f"{self.title} by {self.author}, published in {self.year}"

book1 = Book("1984", "George Orwell", 1949)
book2 = Book("To Kill a Mockingbird", "Harper Lee", 1960)
book3 = Book("The Great Gatsby", "F. Scott Fitzgerald", 1925)
print(book1.get_summary())
print(book2.get_summary())
print(book3.get_summary())