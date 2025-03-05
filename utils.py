from models import Trip, ItineraryItem, Activity
from datetime import datetime
from typing import List


def create_trip_data(location: str, timeOfday: List[str], group: str) -> Trip:
    """Create a trip data object for the given location."""
    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    if location is not None:
        location_str = location
    else:
        location_str = "Unknown"

    if timeOfday is not None:
        time_of_day = ",".join(timeOfday)
    else:
        time_of_day = "Morning,Afternoon,Evening"

    if group is not None:
        group_str = group
    else:
        group_str = "Solo"

    # Create a trip object
    trip = Trip(
        city=location,
        custom_name=f"Trip to {location_str}",
        date_of_trip=current_date,
        time_of_day=time_of_day,
        group=group_str,
    )

    return trip


def activity_to_itinerary(activity: dict) -> ItineraryItem:
    return ItineraryItem(
        title=activity.get("title", ""),
        start=activity.get("start", ""),
        end=activity.get("end", ""),
        description=activity.get("description", ""),
        price=activity.get("price", 0.0),
        theme=activity.get("theme", ""),
        transport=activity.get("transport", False),
        transportMode=activity.get("transport_mode", None),
        requires_booking=activity.get("requires_booking", False),
        booking_url=activity.get("booking_url", None),
        weather=activity.get("weather", None),
        temperature=activity.get("temperature", None),
        image_link=(
            activity.get("image_link", "").split(",")
            if activity.get("image_link")
            else []
        ),
        duration=activity.get("duration", 0),
        id=activity.get("id", 0),
        latitude=activity.get("latitude", None),
        longitude=activity.get("longitude", None),
    )


# Function to convert ItineraryItem -> Activity
def itinerary_to_activity(itinerary: ItineraryItem) -> Activity:
    return Activity(
        title=itinerary.title,
        start=itinerary.start,
        end=itinerary.end,
        description=itinerary.description,
        price=itinerary.price,
        theme=itinerary.theme,
        transport_mode=itinerary.transportMode,
        transport=itinerary.transport,
        requires_booking=itinerary.requires_booking,
        booking_url=itinerary.booking_url,
        weather=itinerary.weather,
        temperature=itinerary.temperature,
        image_link=(
            ",".join(itinerary.image_link) if itinerary.image_link else None
        ),  # Convert list to CSV
        duration=itinerary.duration,
        id=itinerary.id,
        latitude=itinerary.latitude,
        longitude=itinerary.longitude,
    )
