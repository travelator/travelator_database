from fastapi import FastAPI
from pydantic import BaseModel
import requests
import polyline
import folium

# Initialize FastAPI app
app = FastAPI()

# Google Maps API Key (Replace with your actual API key)
GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"

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


# Request model for directions API
class DirectionsRequest(BaseModel):
    origin: list[float]  # [latitude, longitude]
    destination: list[float]  # [latitude, longitude]
    mode: str = (
        "transit"  # Default to transit (options: driving, walking, transit)
    )


# Request model for itinerary map
class ItineraryRequest(BaseModel):
    city: str
    itinerary: list[dict]  # List of places with names & locations


# *Google Directions API - Fetch Route Data**
def get_google_directions(origin, destination, mode="transit"):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": f"{origin[0]},{origin[1]}",
        "destination": f"{destination[0]},{destination[1]}",
        "mode": mode,
        "departure_time": "now",
        "key": GOOGLE_MAPS_API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "OK":
        return None

    routes = []
    for route in data["routes"]:
        legs = route["legs"][0]
        polyline_data = route["overview_polyline"]["points"]
        decoded_polyline = polyline.decode(polyline_data)
        duration = legs["duration"]["text"]
        distance_km = legs["distance"]["value"] / 1000  # Convert meters to km
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


# **API Endpoint: Get Directions**
@app.post("/get-directions")
def get_directions(request: DirectionsRequest):
    route_data = get_google_directions(
        request.origin, request.destination, request.mode
    )
    if not route_data:
        return {"error": "No route found"}

    return {"routes": route_data}


# 🎯 **API Endpoint: Generate Itinerary Map**
@app.post("/get-itinerary-map")
def generate_itinerary_map(request: ItineraryRequest):
    city = request.city
    itinerary = request.itinerary

    if not itinerary:
        return {"error": "Itinerary is missing"}

    start_location = itinerary[0].get("location")
    if not start_location:
        return {"error": "Invalid itinerary format"}

    itinerary_map = folium.Map(location=start_location, zoom_start=13)
    route_layers = {}

    for i in range(len(itinerary) - 1):
        start = itinerary[i]["location"]
        end = itinerary[i + 1]["location"]

        for mode, color in [
            ("driving", "red"),
            ("transit", "blue"),
            ("walking", "green"),
        ]:
            route_data = get_google_directions(start, end, mode)
            if route_data:
                route = route_data[0]
                layer_name = f"{mode.capitalize()} | {itinerary[i]['name']} → {itinerary[i + 1]['name']}"

                if layer_name not in route_layers:
                    route_layers[layer_name] = folium.FeatureGroup(
                        name=layer_name, overlay=True
                    )

                folium.PolyLine(
                    route["polyline"], color=color, weight=3.5
                ).add_to(route_layers[layer_name])

                popup_info = f"""
                <div style="width: 250px; font-size: 14px;">
                    <b style="font-size: 16px;">{mode.capitalize()} Route</b>
                    <br><b>Duration:</b> {route['duration']}
                    <br><b>Route:</b> {route['summary']}
                """

                if mode == "transit":
                    popup_info += f"""
                    <br><b>💰 Fares:</b>
                    <table style="width: 100%; font-size: 14px;">
                        <tr><td>Subway:</td><td>${PUBLIC_TRANSIT_FARES[city]['subway']}</td></tr>
                        <tr><td>Bus:</td><td>${PUBLIC_TRANSIT_FARES[city]['bus']}</td></tr>
                    </table>
                    """
                    for step in route["transit_steps"]:
                        transit_icon = (
                            "🚍 Bus" if step["type"] == "BUS" else "🚇 Subway"
                        )
                        popup_info += f"<br>{transit_icon}: <b>{step['line']}</b> (Departs at {step['departure']})"

                popup_info += "</div>"

                folium.Marker(
                    route["polyline"][len(route["polyline"]) // 2],
                    popup=folium.Popup(popup_info, max_width=300),
                    icon=folium.Icon(color=color, icon="info-sign"),
                ).add_to(route_layers[layer_name])

    for layer in route_layers.values():
        layer.add_to(itinerary_map)

    map_filename = "itinerary_map.html"
    itinerary_map.save(map_filename)

    return {"map_url": f"/static/{map_filename}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
