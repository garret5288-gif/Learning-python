import requests # Import requests for HTTP requests

def random_joke(): # Fetch and display a random joke
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    if response.status_code == 200: # Successful response
        data = response.json() # Parse JSON data
        print(f"{data['setup']}\n{data['punchline']}")
    else: # Handle errors
        print(f"Error: Unable to fetch joke {response.status_code}")

random_joke()