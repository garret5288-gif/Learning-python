import requests

def fetch_fake_user(): # Fetch and display a fake user profile
    response = requests.get("https://randomuser.me/api/") # Make GET request to Random User API
    if response.status_code == 200: # Successful response
        data = response.json() # Parse JSON data
        user = data['results'][0] # Extract user information
        name = user['name'] # Extract name details
        location = user['location'] # Extract location details
        print(f"Name: {name['title']} {name['first']} {name['last']}")
        print(f"Email: {user['email']}")
        print(f"Location: {location['city']}, {location['country']}")
    else:
        print(f"Error: Unable to fetch user data {response.status_code}")
fetch_fake_user()