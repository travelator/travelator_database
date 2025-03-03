import requests
import json

BASE_URL = "http://0.0.0.0:8080"  # change to actual working base url

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


headers = {"Content-Type": "application/json"}
cookies = {"token": token_cookie}
response = requests.post(f"{BASE_URL}/save", data=json.dumps(trip_data), headers=headers, cookies=cookies)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")

trip_id = response.json().get("trip_id")

if not trip_id:
    print("Failed to get trip_id from save response")
    exit(1)

response = requests.get(f"{BASE_URL}/trips", headers=headers, cookies=cookies)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")

view_response = requests.get(f"{BASE_URL}/trips/{trip_id}", headers=headers, cookies=cookies)
print(f"View Single Trip Status Code: {view_response.status_code}")
print(f"View Single Trip Response: {view_response.json()}")

updated_trip_data = {
    "trip": {
        "city": "Krakow",
        "custom_name": "Updated Test Trip",
        "date_of_trip": "2025-04-01",
        "time_of_day": "Afternoon",
        "group": "Family"
    },
    "activities": [
        {
            "title": "Castle Tour",
            "start": "2:00 PM",
            "end": "4:00 PM",
            "description": "Visit to Wawel Castle",
            "price": 15.0,
            "theme": "History",
            "transport_mode": "Walk",
            "requires_booking": True,
            "image_link": "",
            "duration": 120,
            "weather": "Sunny",
            "id": 1,
            "booking_url": "https://wawel.krakow.pl"
        },
        {
            "title": "Traditional Polish Dinner",
            "start": "7:00 PM",
            "end": "9:00 PM",
            "description": "Enjoy traditional Polish cuisine",
            "price": 30.0,
            "theme": "Food",
            "transport_mode": "Taxi",
            "requires_booking": True,
            "booking_url": "https://restaurant.krakow.pl",
            "image_link": "",
            "duration": 120,
            "weather": "",
            "id": 2
        }
    ]
}

edit_response = requests.put(f"{BASE_URL}/trips/{trip_id}", data=json.dumps(updated_trip_data), headers=headers, cookies=cookies)

print(f"Edit Trip Status Code: {edit_response.status_code}")
print(f"Edit Trip Response: {edit_response.json()}")

delete_response = requests.delete(f"{BASE_URL}/trips/{trip_id}", headers=headers, cookies=cookies)
print(f"Delete Trip Status Code: {delete_response.status_code}")
print(f"Delete Trip Response: {delete_response.json()}")

# Attempt to view the deleted trip (should return 404)
view_deleted_response = requests.get(f"{BASE_URL}/trips/{trip_id}", headers=headers, cookies=cookies)
print(f"View Deleted Trip Status Code: {view_deleted_response.status_code}")
print(f"View Deleted Trip Response: {view_deleted_response.json()}")
