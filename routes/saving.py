from fastapi import APIRouter, HTTPException, Depends, Cookie
from fastapi.security import APIKeyCookie
import requests
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from uuid import UUID
from models.models import (
    FullItinerary,
)
from utils.utils import (
    create_trip_data,
    itinerary_to_activity,
    activity_to_itinerary,
)
import json

load_dotenv()

url: str = os.getenv("PROJECT_URL")
key: str = os.getenv("API_KEY")
auth_url: str = os.getenv("AUTH_URL")

supabase: Client = create_client(url, key)

router = APIRouter()

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
    trip_request: FullItinerary,
    user_id: str = Depends(get_current_user),
    searchConfig: str = Cookie(None),
):

    # Look for cookie data on search parameters
    try:
        cookie_data = json.loads(searchConfig)
    except json.JSONDecodeError:
        cookie_data = {}

    location = cookie_data.get("city", None)
    timeOfDay = cookie_data.get("timeOfDay", None)
    group = cookie_data.get("group", None)
    date = cookie_data.get("date", None)

    trip = create_trip_data(location, timeOfDay, group, date).model_dump()
    trip["user_id"] = user_id
    trip_response = supabase.table("trips").insert(trip).execute()

    # Convert acitivity to the correct format (comma separated lists rather than str)
    activities = [
        itinerary_to_activity(activity).model_dump()
        for activity in trip_request.itinerary
    ]

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
            trip["timeOfDay"] = trip["time_of_day"].split(",")

            # Fetch activities for the current trip
            activities_response = (
                supabase.table("activities")
                .select("*")
                .eq("trip_id", trip_id)
                .execute()
            )

            # Add activities to the trip object
            activities = (
                activities_response.data if activities_response.data else []
            )

            # reformat to correct type
            activities_db = [
                activity_to_itinerary(activity) for activity in activities
            ]

            trip["itinerary"] = activities_db

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

        trip["activities"] = (
            activities_response.data if activities_response.data else []
        )

        return trip

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/trips/{trip_id}")
async def edit_trip(
    trip_id: UUID,
    trip_update_request: FullItinerary,
    user_id: str = Depends(get_current_user),
):

    # Convert acitivity to the correct format (comma separated lists rather than str)
    activities = [
        itinerary_to_activity(activity).model_dump()
        for activity in trip_update_request.itinerary
    ]

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

    if activities:
        supabase.table("activities").delete().eq(
            "trip_id", str(trip_id)
        ).execute()

        for activity in activities:
            activity["trip_id"] = str(trip_id)

        supabase.table("activities").insert(activities).execute()

    return {"success": "Trip and activities updated successfully"}


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
