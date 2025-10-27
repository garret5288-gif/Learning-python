import os
import requests

def fetch_fake_user(): # Fetch and display a fake user profile
    response = requests.get("https://randomuser.me/api/")
    if response.status_code == 200:
        data = response.json() # Parse JSON data
        user = data['results'][0]
        name = user['name']
        location = user['location']
        print(f"Name: {name['title']} {name['first']} {name['last']}")
        print(f"Email: {user['email']}")
        print(f"Location: {location['city']}, {location['country']}")
        return location.get('city') # Return city for weather lookup
    else:
        print(f"Error: Unable to fetch user data {response.status_code}")
        return None # Return None if user data fetch fails

def random_joke(): # Fetch and display a random joke
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    if response.status_code == 200:
        data = response.json() # Parse JSON data
        print(f"{data['setup']}\n{data['punchline']}")
    else:
        print(f"Error: Unable to fetch joke {response.status_code}")

def current_weather(city): # Fetch and display current weather for a city
    key_path = os.path.join(os.path.dirname(__file__), "weather_api_key.txt") # Path to API key file
    try: # Load API key from file
        api_key = open(key_path).read().strip()
    except FileNotFoundError: # Handle missing key file
        print(f"Missing API key file: {key_path}. Create it and put your OpenWeather key inside.")
        return

    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather", # Base URL for OpenWeather API
        params={"q": city, "appid": api_key, "units": "imperial"},
        timeout=10,
    )
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        print(f"Current weather in {data['name']}: {weather}, Temperature: {temp}°F")
    else:
        print(f"Error: Unable to fetch weather data for {city} {response.status_code}")

if __name__ == "__main__":
    city = fetch_fake_user() # Fetch fake user and get their city
    if city: # If city is available
        current_weather(city) # Fetch and display current weather
        print("their favoritejoke is:")
        random_joke()