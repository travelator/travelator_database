from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import APIKeyCookie
from pydantic import BaseModel
from typing import List
import requests
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("PROJECT_URL")
key: str = os.getenv("API_KEY")
auth_url: str = os.getenv("AUTH_URL")

supabase: Client = create_client(url, key)

router = APIRouter()


class Activity(BaseModel):
    title: str
    start: str
    end: str
    description: str
    price: float
    theme: str
    transport_mode: str
    requires_booking: bool
    image_link: str
    duration: int
    weather: str
    id: int
    booking_url: str = ""


class Trip(BaseModel):
    city: str
    custom_name: str
    date_of_trip: str
    time_of_day: str
    group: str


class TripRequest(BaseModel):
    trip: Trip
    activities: List[Activity]


cookie_sec = APIKeyCookie(name="token")


def get_current_user(token: str = Depends(cookie_sec)):
    validate_response = requests.get(f"{auth_url}/validate", cookies={"token": token})
    if validate_response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    return validate_response.json().get("user_id")


@router.post("/save")
async def save_trip(trip_request: TripRequest, user_id: str = Depends(get_current_user)):
    trip = trip_request.model_dump().get("trip")
    print(trip)
    activities = [activity.model_dump() for activity in trip_request.activities]
    trip["user_id"] = user_id

    try:
        trip_response = (supabase
                         .table("trips")
                         .insert(trip)
                         .execute())

        if not trip_response.data:
            raise HTTPException(status_code=500, detail=f"Failed to insert trip: {trip_response.status_code}")

        trip_id = trip_response.data[0]["trip_id"]

        for activity in activities:
            activity["trip_id"] = trip_id

        activities_response = (supabase
                               .table("activities")
                               .insert(activities)
                               .execute())

        if not activities_response.data:
            raise HTTPException(status_code=500, detail=f"Failed to insert activities: {activities_response.status_code}")

        return {"success": "Trip and activities added successfully", "trip_id": trip_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trips")
async def get_trips(user_id: str = Depends(get_current_user)):
    try:

        trips_response = supabase.table("trips").select("*").eq("user_id", user_id).execute()

        if not trips_response.data:
            return {"message": f"No trips found for user ID {user_id}"}

        trips = trips_response.data

        trip_activities = {}

        for trip in trips:
            trip_id = trip["trip_id"]
            trip_name = trip["custom_name"]

            activities_response = supabase.table("activities").select("*").eq("trip_id", trip_id).order("id").execute()

            if not activities_response.data:
                trip_activities[trip_name] = ["No activities found"]
            else:
                activities = activities_response.data
                activity_names = [activity["title"] for activity in activities]
                trip_activities[trip_name] = activity_names

        return {"user_id": user_id, "trips": trip_activities}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
