# Iterating through dictionaries

movie_time = {"Inception": '8:00 PM', 
              "The Matrix": '9:30 PM', 
              "Interstellar": '7:45 PM',
              "The Dark Knight": '10:15 PM'
}

for movie, time in movie_time.items(): # iterating through both keys and values and unpacking them
    print(f"{movie} starts at {time}")

for movie in movie_time.keys(): # iterating through keys
    print(movie)
for time in movie_time.values(): # iterating through values
    print(time)
for a, b in movie_time.items(): # iterating through both keys and values
    print(a, b)