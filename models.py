from pydantic import BaseModel, Field, HttpUrl
from enum import Enum
from typing import List


class Theme(str, Enum):
    ADVENTURE = "Adventure"
    CULTURE = "Culture"
    FOOD_DRINK = "Food and drink"
    NATURE = "Nature"
    RELAXATION = "Relaxation"
    ENTERTAINMENT = "Entertainment"
    SHOPPING = "Shopping"
    SPORTS = "Sports"
    FAMILY = "Family"
    UNIQUE = "Unique"
    NIGHTLIFE = "Nightlife"


class ActivityRequest(BaseModel):
    city: str
    timeOfDay: List[str]
    group: str


class Preference(BaseModel):
    disliked: List[str]
    liked: List[str]


class RateCard(BaseModel):
    city: str
    preferences: List[Preference]


class TransportMode(str, Enum):
    TUBE = "Tube"
    WALKING = "Walking"
    BUS = "Bus"
    TAXI = "Taxi"
    TRAIN = "Train"
    FERRY = "Ferry"
    DEFAULT = "N/A"


class Activity(BaseModel):
    """An activity that could be part of an itinerary"""

    id: int = Field(description="Unique identifier for the activity.")
    title: str = Field(description="Title of the activity.")
    description: str = Field(
        description="Detailed description of the activity."
    )
    image_link: List[str] = Field(
        description="URL to an image representing the activity."
    )
    price: float = Field(
        description="Cost of the itinerary item, in GBP. If free, write 0."
    )
    theme: Theme = Field(description="Theme of the activity.")


class ItineraryItem(BaseModel):
    """An entry for an itinerary item"""

    title: str = Field(description="Title of the itinerary item.")
    transport: bool = Field(
        description="Only TRUE if the itinerary item is not an actual activity of any kind but is just transport from one location to another."
    )
    start: str = Field(description="Start time of the itinerary item.")
    end: str = Field(description="End time of the itinerary item.")
    description: str = Field(
        description="Detailed description of the itinerary item."
    )
    price: float = Field(
        description="Cost of the itinerary item, in GBP. If free, write 0."
    )
    theme: Theme = Field(description="Theme of the itinerary item.")
    transportMode: TransportMode = Field(
        description="Mode of transport if it is a transport step. Only required if it is transport."
    )
    requires_booking: bool = Field(
        description="Indicates if the item requires booking."
    )
    booking_url: HttpUrl = Field(
        description="URL for booking the itinerary item."
    )
    image: HttpUrl = Field(
        description="URL to an image representing the itinerary item."
    )
    duration: int = Field(
        description="Duration of the itinerary item in minutes."
    )
    id: int = Field(description="Unique identifier for the itinerary item.")


class ActivityList(BaseModel):
    activities: list[Activity] = Field(description="List of activities.")


class FullItinerary(BaseModel):
    itinerary: list[ItineraryItem] = Field(
        description="A full day itinerary for the given location"
    )
