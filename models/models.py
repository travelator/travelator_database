from pydantic import BaseModel, Field
from typing import List, Optional


class ItineraryItem(BaseModel):
    """An entry for an itinerary item"""

    title: str = Field(description="Brief title of the itinerary item.")
    transport: bool = Field(
        description="Only TRUE if the itinerary item is not an actual activity of any kind but is just transport from one location to another."
    )
    start: str = Field(description="Start time of the itinerary item.")
    end: str = Field(description="End time of the itinerary item.")
    description: str = Field(
        description="Brief description of the activity - maximum two sentences."
    )
    price: float = Field(
        description="Cost of the itinerary item, in GBP. If free, write 0."
    )
    theme: str = Field(description="Theme of the itinerary item.")
    transportMode: str = Field(
        description="Mode of transport if it is a transport step. Only required if it is transport. MUST Be one of the following: Tube, Walking, Bus, Taxi, Train, Ferry, N/A"
    )
    requires_booking: bool = Field(
        description="Indicates if the item requires booking."
    )
    booking_url: Optional[str] = Field(
        default=None, description="URL for booking the itinerary item."
    )
    weather: Optional[str] = Field(
        default=None,
        description="Weather conditions for the given activity. Do not generate.",
    )
    temperature: Optional[int] = Field(
        default=None,
        description="Temperature in celsius for the given activity. Do not generate.",
    )
    image_link: List[str] = Field(
        default=[],
        description="URLs of images representing the activity. Do not generate.",
    )
    duration: int = Field(
        description="Duration of the itinerary item in minutes."
    )
    id: int = Field(description="Unique identifier for the itinerary item.")
    latitude: Optional[float] = Field(
        default=None, description="Latitude position of the given activity."
    )
    longitude: Optional[float] = Field(
        default=None, description="Longitude position of the given activity."
    )


class FullItinerary(BaseModel):
    itinerary: list[ItineraryItem] = Field(
        description="A full day itinerary for the given location"
    )


class Activity(BaseModel):
    title: str
    start: str
    end: str
    description: str
    price: float
    theme: str
    transport_mode: Optional[str]
    transport: bool
    requires_booking: bool
    image_link: Optional[str]
    duration: int
    weather: Optional[str]
    temperature: Optional[int]
    id: int
    booking_url: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]


class Trip(BaseModel):
    city: str
    custom_name: str
    date_of_trip: str
    time_of_day: str
    group: str


class TripRequest(BaseModel):
    trip: Trip
    activities: List[Activity]


class TripUpdateRequest(BaseModel):
    trip: Trip
    activities: Optional[List[Activity]] = None


class DirectionsRequest(BaseModel):
    origin: list[float]  # [latitude, longitude]
    destination: list[float]  # [latitude, longitude]
    mode: str = (
        "transit"  # Default to transit (options: driving, walking, transit)
    )


class ItineraryRequest(BaseModel):
    city: str
    itinerary: list[dict]  # List of places with names & locations
