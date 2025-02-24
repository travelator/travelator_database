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


class TestActivityRequest:
    def test_valid_request(self):
        request = ActivityRequest(
            city="London", timeOfDay=["Morning", "Afternoon"], group="Family"
        )
        assert request.city == "London"
        assert request.timeOfDay == ["Morning", "Afternoon"]
        assert request.group == "Family"

    def test_invalid_city_type(self):
        with pytest.raises(ValidationError):
            ActivityRequest(
                city=123,  # Should be string
                timeOfDay=["Morning"],
                group="Family",
            )

    def test_invalid_time_of_day_type(self):
        with pytest.raises(ValidationError):
            ActivityRequest(
                city="London",
                timeOfDay="Morning",  # Should be list
                group="Family",
            )


class TestPreference:
    def test_valid_preference(self):
        pref = Preference(
            title=["Test Activity 1", "Test Activity 2"],
            liked=["Activity 3", "Activity 4"],
            disliked=["Activity 5", "Activity 6"],
        )
        assert isinstance(pref.liked, list)
        assert isinstance(pref.disliked, list)
        assert len(pref.liked) == 2
        assert len(pref.disliked) == 2

    def test_invalid_liked_type(self):
        with pytest.raises(ValidationError):
            Preference(liked="not a list", disliked=["Activity 1"])

    def test_invalid_disliked_type(self):
        with pytest.raises(ValidationError):
            Preference(liked=["Activity 1"], disliked="not a list")


class TestRateCard:
    def test_valid_rate_card(self):
        preferences = [
            Preference(
                liked=["Activity 1", "Activity 2"], disliked=["Activity 3"]
            )
        ]
        rate_card = RateCard(city="London", preferences=preferences)
        assert rate_card.city == "London"
        assert len(rate_card.preferences) == 1
        assert len(rate_card.preferences[0].liked) == 2
        assert len(rate_card.preferences[0].disliked) == 1

    def test_invalid_city_type(self):
        with pytest.raises(ValidationError):
            RateCard(
                city=123,  # Should be string
                preferences=[
                    Preference(liked=["Activity 1"], disliked=["Activity 2"])
                ],
            )


class TestActivity:
    def test_valid_activity(self):
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

    def test_invalid_theme(self):
        with pytest.raises(ValidationError):
            Activity(
                id=1,
                title="Test",
                description="Test",
                image_link="https://example.com/image.jpg",
                price=10.50,
                theme="Invalid Theme",  # Should be Theme enum
            )

    def test_invalid_url(self):
        with pytest.raises(ValidationError):
            Activity(
                id=1,
                title="Test",
                description="Test",
                image_link="not-a-url",  # Should be valid URL
                price=10.50,
                theme=Theme.ADVENTURE,
            )


class TestItineraryItem:
    def test_valid_item(self):
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
        assert item.theme == Theme.CULTURE
        assert item.transportMode == TransportMode.DEFAULT

    def test_transport_item(self):
        item = ItineraryItem(
            title="Transport",
            transport=True,
            start="09:00",
            end="10:00",
            description="Transport item",
            price=15.00,
            theme=Theme.ADVENTURE,
            transportMode=TransportMode.TUBE,
            requires_booking=False,
            booking_url="https://example.com/booking",
            image="https://example.com/image.jpg",
            duration=60,
            id=1,
        )
        assert item.transport is True
        assert item.transportMode == TransportMode.TUBE


class TestActivityList:
    def test_valid_list(self):
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


class TestFullItinerary:
    def test_valid_itinerary(self):
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
