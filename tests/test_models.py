import pytest
from pydantic import ValidationError
from models import (
    Theme,
    ActivityRequest,
    Preference,
    RateCard,
    TransportMode,
    Activity,
    ItineraryItem,
    ActivityList,
    FullItinerary,
)


def test_activity_request_valid():
    request = ActivityRequest(
        city="London", timeOfDay=["Morning", "Afternoon"], group="Family"
    )
    assert request.city == "London"
    assert request.timeOfDay == ["Morning", "Afternoon"]
    assert request.group == "Family"


def test_preference_valid():
    pref = Preference(title="Test Activity", liked=True)
    assert pref.title == "Test Activity"
    assert pref.liked is True


def test_rate_card_valid():
    preferences = [
        Preference(title="Activity 1", liked=True),
        Preference(title="Activity 2", liked=False),
    ]
    rate_card = RateCard(city="London", preferences=preferences)
    assert rate_card.city == "London"
    assert len(rate_card.preferences) == 2
    assert rate_card.preferences[0].liked is True
    assert rate_card.preferences[1].liked is False


def test_activity_valid():
    activity = Activity(
        id=1,
        title="Test Activity",
        description="A test activity description",
        image_link="https://example.com/image.jpg",
        price=10.50,
        theme=Theme.ADVENTURE,
    )
    assert activity.id == 1
    assert activity.title == "Test Activity"
    assert activity.price == 10.50
    assert activity.theme == Theme.ADVENTURE


def test_itinerary_item_valid():
    item = ItineraryItem(
        title="Test Item",
        transport=False,
        start="09:00",
        end="10:00",
        description="A test itinerary item",
        price=15.00,
        theme=Theme.CULTURE,
        transportMode=TransportMode.DEFAULT,
        requires_booking=False,
        booking_url="https://example.com/booking",
        image="https://example.com/image.jpg",
        duration=60,
        id=1,
    )
    assert item.title == "Test Item"
    assert item.transport is False
    assert item.duration == 60


def test_activity_list_valid():
    activities = [
        Activity(
            id=1,
            title="Activity 1",
            description="Description 1",
            image_link="https://example.com/image1.jpg",
            price=10.00,
            theme=Theme.ADVENTURE,
        ),
        Activity(
            id=2,
            title="Activity 2",
            description="Description 2",
            image_link="https://example.com/image2.jpg",
            price=20.00,
            theme=Theme.CULTURE,
        ),
    ]
    activity_list = ActivityList(activities=activities)
    assert len(activity_list.activities) == 2


def test_full_itinerary_valid():
    items = [
        ItineraryItem(
            title="Item 1",
            transport=False,
            start="09:00",
            end="10:00",
            description="Description 1",
            price=15.00,
            theme=Theme.ADVENTURE,
            transportMode=TransportMode.DEFAULT,
            requires_booking=False,
            booking_url="https://example.com/booking1",
            image="https://example.com/image1.jpg",
            duration=60,
            id=1,
        )
    ]
    itinerary = FullItinerary(itinerary=items)
    assert len(itinerary.itinerary) == 1


def test_invalid_activity_request():
    with pytest.raises(ValidationError):
        ActivityRequest(
            city=123,  # Should be string
            timeOfDay="Morning",  # Should be list
            group="Family",
        )


def test_invalid_activity():
    with pytest.raises(ValidationError):
        Activity(
            id="1",  # Should be integer
            title=123,  # Should be string
            description="Description",
            image_link="not-a-url",  # Should be valid URL
            price="10.50",  # Should be float
            theme="Invalid Theme",  # Should be valid Theme enum
        )
