from fastapi import APIRouter
import requests
import polyline
import os
from models.models import DirectionsRequest

# Create a router
router = APIRouter()

# Google Maps API Key (Replace with your actual API key)
GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Taxi fare data
TAXI_FARES = {
    "New York City": {"base_fare": 3.00, "per_km": 1.50},
    "London": {"base_fare": 3.20, "per_km": 2.00},
    "San Francisco": {"base_fare": 3.50, "per_km": 2.25},
}

# Public transport fare data
PUBLIC_TRANSIT_FARES = {
    "New York City": {"bus": 2.75, "subway": 2.75},
    "London": {"bus": 1.75, "subway": 2.40},
    "San Francisco": {"bus": 3.00, "subway": 3.50},
}


# Google Directions API - Fetch Route Data
def get_google_directions(origin, destination, mode="transit"):
    print(f"Getting directions from {origin} to {destination}, mode: {mode}")

    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": f"{origin[0]},{origin[1]}",
        "destination": f"{destination[0]},{destination[1]}",
        "mode": mode,
        "departure_time": "now",
        "key": GOOGLE_MAPS_KEY,
    }

    print(f"Google API request params: {params}")

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") != "OK":
            return None

        print(f"Google API response status: {data.get('status')}")
        if data.get("status") != "OK":
            print(
                f"Error message: {data.get('error_message', 'No specific error message')}"
            )

        routes = []
        for route in data["routes"]:
            legs = route["legs"][0]
            polyline_data = route["overview_polyline"]["points"]
            decoded_polyline = polyline.decode(polyline_data)
            duration = legs["duration"]["text"]
            distance_km = (
                legs["distance"]["value"] / 1000
            )  # Convert meters to km
            summary = route.get("summary", "Multiple Roads")

            transit_steps = []
            for step in legs["steps"]:
                if "transit_details" in step:
                    line_name = step["transit_details"]["line"]["short_name"]
                    transit_type = step["transit_details"]["line"]["vehicle"][
                        "type"
                    ]
                    departure_time = step["transit_details"]["departure_time"][
                        "text"
                    ]
                    transit_steps.append(
                        {
                            "line": line_name,
                            "type": transit_type,
                            "departure": departure_time,
                        }
                    )

            routes.append(
                {
                    "polyline": decoded_polyline,
                    "duration": duration,
                    "summary": summary,
                    "distance_km": distance_km,
                    "transit_steps": transit_steps,
                }
            )

        return routes

    except Exception as e:
        print(f"Error fetching directions: {e}")
        return None


# API Endpoint: Get Directions
@router.post("/get-directions")
def get_directions(request: DirectionsRequest):
    route_data = get_google_directions(
        request.origin, request.destination, request.mode
    )
    if not route_data:
        return {"error": "No route found"}

    return {"routes": route_data}
