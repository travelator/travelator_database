from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import APIKeyCookie
from pydantic import BaseModel
from typing import List, Optional
import requests
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from uuid import UUID

# from utils import convert_array_to_string, convert_string_to_array
from models import SaveRequest

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
    transport: bool
    requires_booking: bool
    image_link: str
    duration: int
    weather: str
    temperature: int
    id: int
    booking_url: str
    longitude: float
    latitude: float


class Trip(BaseModel):
    city: str
    custom_name: str
    date_of_trip: str
    date_created: str
    time_of_day: str
    group: str
    uniqueness: int


class TripRequest(BaseModel):
    trip: Trip
    activities: List[Activity]


class TripUpdateRequest(BaseModel):
    trip: Trip
    activities: Optional[List[Activity]] = None


cookie_sec = APIKeyCookie(name="token")


def get_current_user(token: str = Depends(cookie_sec)):
    validate_response = requests.get(
        f"{auth_url}/validate", cookies={"token": token}
    )
    if validate_response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    return validate_response.json().get("user_id")


@router.post("/save")
async def save_trip(
    trip_request: SaveRequest, user_id: str = Depends(get_current_user)
):

    trip = trip_request.model_dump().get("trip")
    print(trip)
    itinerary = [item.model_dump() for item in trip_request.itinerary]
    trip["user_id"] = user_id

    for item in itinerary:
        original_image_links = item["image_link"]
        item["image_link"] = ",".join(
            item["image_link"]
        )  # Convert array to string
        return print(
            f"Original image_link: {original_image_links} -> Converted image_link: {item['image_link']}"
        )


"""
    try:
        trip_response = supabase.table("trips").insert(trip).execute()

        if not trip_response.data:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to insert trip: {trip_response.status_code}",
            )

        trip_id = trip_response.data[0]["trip_id"]

        for activity in activities:
            activity["trip_id"] = trip_id

        activities_response = (
            supabase.table("activities").insert(activities).execute()
        )

        if not activities_response.data:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to insert activities: {activities_response.status_code}",
            )

        return {
            "success": "Trip and activities added successfully",
            "trip_id": trip_id,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""


@router.get("/trips")
async def get_trips(user_id: str = Depends(get_current_user)):
    try:
        trips_response = (
            supabase.table("trips")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )

        if not trips_response.data:
            return {"message": f"No trips found for user ID {user_id}"}

        trips = trips_response.data

        trips_with_activities = []

        for trip in trips:
            trip_id = trip["trip_id"]

            # Fetch activities for the current trip
            activities_response = (
                supabase.table("activities")
                .select("*")
                .eq("trip_id", trip_id)
                .execute()
            )
            if activities_response.data:
                for activity in activities_response.data:
                    # Convert image_link back from string to list
                    activity["image_link"] = activity["image_link"].split(
                        ","
                    )  # Convert string back to list

            # Add activities to the trip object
            trip["activities"] = (
                activities_response.data if activities_response.data else []
            )

            trips_with_activities.append(trip)

        return {"user_id": user_id, "trips": trips_with_activities}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trips/{trip_id}")
async def get_single_trip(
    trip_id: UUID, user_id: str = Depends(get_current_user)
):
    try:
        trip_response = (
            supabase.table("trips")
            .select("*")
            .eq("trip_id", str(trip_id))
            .eq("user_id", user_id)
            .execute()
        )

        if not trip_response.data:
            raise HTTPException(
                status_code=404,
                detail="Trip not found or does not belong to the user",
            )

        trip = trip_response.data[0]

        activities_response = (
            supabase.table("activities")
            .select("*")
            .eq("trip_id", str(trip_id))
            .execute()
        )

        if activities_response.data:
            for activity in activities_response.data:
                # Convert image_link back from string to list
                activity["image_link"] = activity["image_link"].split(
                    ","
                )  # Convert string back to list

        trip["activities"] = (
            activities_response.data if activities_response.data else []
        )

        return trip

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/trips/{trip_id}")
async def edit_trip(
    trip_id: UUID,
    trip_update_request: TripUpdateRequest,
    user_id: str = Depends(get_current_user),
):
    try:
        trip_response = (
            supabase.table("trips")
            .select("*")
            .eq("trip_id", trip_id)
            .eq("user_id", user_id)
            .execute()
        )

        if not trip_response.data:
            raise HTTPException(
                status_code=404,
                detail="Trip not found or does not belong to the user",
            )

        if trip_update_request.trip:
            update_data = {
                k: v
                for k, v in trip_update_request.trip.model_dump().items()
                if v is not None
            }
            if update_data:
                supabase.table("trips").update(update_data).eq(
                    "trip_id", str(trip_id)
                ).execute()

        if trip_update_request.activities:
            supabase.table("activities").delete().eq(
                "trip_id", str(trip_id)
            ).execute()

            new_activities = [
                activity.model_dump()
                for activity in trip_update_request.activities
            ]
            for activity in new_activities:
                activity_data = activity.model_dump()
                if activity_data.get("image_link"):
                    activity_data["image_link"] = ",".join(
                        activity_data["image_link"]
                    )
                activity["trip_id"] = str(trip_id)
                new_activities.append(activity_data)

            supabase.table("activities").insert(new_activities).execute()

        return {"success": "Trip and activities updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/trips/{trip_id}")
async def delete_trip(trip_id: UUID, user_id: str = Depends(get_current_user)):
    try:
        trip_response = (
            supabase.table("trips")
            .select("*")
            .eq("trip_id", str(trip_id))
            .eq("user_id", user_id)
            .execute()
        )

        if not trip_response.data:
            raise HTTPException(
                status_code=404,
                detail="Trip not found or does not belong to the user",
            )

        supabase.table("activities").delete().eq(
            "trip_id", str(trip_id)
        ).execute()

        trip_delete_response = (
            supabase.table("trips")
            .delete()
            .eq("trip_id", str(trip_id))
            .execute()
        )

        if trip_delete_response.data:
            return {
                "success": "Trip and associated activities deleted successfully"
            }
        else:
            raise HTTPException(
                status_code=500, detail="Failed to delete the trip"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
