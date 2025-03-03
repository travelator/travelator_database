import requests
import json

BASE_URL = "http://0.0.0.0:5000"  # change to actual working base url

# Login to get the session cookie
login_url = "https://travelator-auth.ambitioussand-14e274b0.uksouth.azurecontainerapps.io/login"
login_data = {"email": "testuser16@example.com", "password": "admin"}
login_response = requests.post(login_url, json=login_data)

if login_response.status_code != 200:
    print(f"Login failed: {login_response.status_code}")
    exit(1)

token_cookie = login_response.cookies.get("token")

# Prepare the trip data
trip_data = {
    "trip": {
        "city": "Warsaw",
        "custom_name": "Test trip 3",
        "date_of_trip": "2025-03-15",
        "time_of_day": "Morning",
        "group": "Friends"
    },
    "activities": [
        {
            "title": "Museum Visit",
            "start": "10:00 AM",
            "end": "12:00 PM",
            "description": "Visit to the Polish Museum",
            "price": 0.0,
            "theme": "Culture",
            "transport_mode": "Walk",
            "requires_booking": False,
            "image_link": "",
            "duration": 2,
            "weather": "Sunny",
            "id": 1
        },
        {
            "title": "Lunch at Local Restaurant",
            "start": "1:00 PM",
            "end": "2:30 PM",
            "description": "Enjoy local pierogi",
            "price": 25.0,
            "theme": "Food",
            "transport_mode": "Walk",
            "requires_booking": True,
            "booking_url": "",
            "image_link": "",
            "duration": 90,
            "weather": "",
            "id": 2
        }
    ]
}

# Send POST request to save the trip
headers = {"Content-Type": "application/json"}
cookies = {"token": token_cookie}
response = requests.post(f"{BASE_URL}/save", data=json.dumps(trip_data), headers=headers, cookies=cookies)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")

response = requests.get(f"{BASE_URL}/trips", headers=headers, cookies=cookies)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
