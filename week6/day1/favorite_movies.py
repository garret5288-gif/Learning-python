# favorite movie collector that allows adding, removing, viewing, and clearing favorite movies

def main(): # Main function to run the favorite movies collector
    favorite_movies = [] # Initialize empty list for favorite movies
    while True: # Main menu loop
        print("Favorite Movies Collector")
        print("1. Add Movie")
        print("2. Remove Movie")
        print("3. View Movies")
        print("4. Clear Movies")
        print("5. Exit")
    
        choice = input("Choose an option (1-5): ") # Get user choice
        # Handle user choices
        if choice == '1':
            add_movie(favorite_movies)
        elif choice == '2':
            remove_movie(favorite_movies)
        elif choice == '3':
            view_movies(favorite_movies)
        elif choice == '4':
            clear_movies(favorite_movies)
        elif choice == '5':
            print("Exiting the Favorite Movies Collector.")
            break # Exit the program
        else: # Handle invalid input
            print("Invalid option. Please try again.")

def add_movie(movies): # Add movies to the favorite movies list
    while True:
        movie = input("Enter a movie to add (or type 'done' to finish): ")
        if movie.lower() == 'done' or movie == '': # Check for 'done' or empty input
            break # Exit loop
        movies.append(movie)
        print(f'Added {movie}. Current movies: {movies}') # Confirm addition

def remove_movie(movies): # Remove movies from the favorite movies list
    while True:
        movie = input("Enter a movie to remove (or type 'done' to finish): ")
        if movie.lower() == 'done' or movie == '':
            break # Exit loop
        if movie in movies:
            movies.remove(movie)
            print(f'Removed {movie}. Current movies: {movies}')
        else: # Movie not found
            print(f"{movie} not found in the list.")

def view_movies(movies): # View the current list of favorite movies
    if movies: # Check if the list is not empty
        print("Favorite Movies:")
        for idx, movie in enumerate(movies, start=1): # Enumerate movies
            print(f"{idx}. {movie}")
    else:
        print("No favorite movies found.")

def clear_movies(movies): # Clear the entire favorite movies list
    movies.clear()
    print("Cleared all favorite movies.")

main() # Run the main function
