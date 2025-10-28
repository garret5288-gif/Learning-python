import os # Import os for file path handling
import requests # Import requests for HTTP requests

key_path = os.path.join(os.path.dirname(__file__), "weather_api_key.txt")
try: # Load API key from file
    api_key = open(key_path).read().strip()
except FileNotFoundError: # Handle missing key file
    raise SystemExit(f"Missing API key file: {key_path}. Create it and put your OpenWeather key inside.")

base_url = "https://api.openweathermap.org/data/2.5/weather"

def current_weather(location): # Fetch and display current weather for a location
    response = requests.get(f"{base_url}?q={location}&appid={api_key}&units=imperial")
    if response.status_code == 200: # Successful response
        data = response.json() # Parse JSON data
        print(f"Location: {data['name']}, {data['sys']['country']}")
        print(f"Temperature: {data['main']['temp']}°F")
        print(f"Condition: {data['weather'][0]['description']}")
    else: # Handle errors
        print(f"Error: Unable to fetch data {response.status_code}")

current_weather("plant city")