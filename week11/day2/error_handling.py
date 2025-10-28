import requests
# Example URL that may fail
url = "https://notreal.example.com/data" 

try: # Attempt to fetch data from the URL
    response = requests.get(url, timeout=5)  
    response.raise_for_status()  
    data = response.json()  
    print("Data fetched successfully:", data)
except requests.exceptions.RequestException as e: # Handle request errors
    print(f"Error fetching data from {url}: {e}")
except ValueError as e: # Handle JSON parsing errors
    print(f"Error parsing JSON data: {e}")
