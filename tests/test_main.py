import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
# import httpx
from main import app


client = TestClient(app)


@pytest.fixture
def mock_http_client():
    with patch("main.http_client") as mock:
        mock.post = AsyncMock()
        yield mock


class TestActivitiesEndpoint:
    """
    def test_success(self, mock_http_client):
        # Mock response data
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "activities": [
                {
                    "id": 1,
                    "title": "Test Activity",
                    "description": "Test Description",
                    "image_link": ["https://example.com/image.jpg"],
                    "price": 10.50,
                    "theme": "Adventure",
                }
            ]
        }
        mock_http_client.post.return_value = mock_response

        # Test data
        test_data = {
            "city": "London",
            "timeOfDay": ["Morning"],
            "group": "Family",
        }

        # Make request
        response = client.post("/activities", json=test_data)

        # Assertions
        assert response.status_code == 200
        assert "activities" in response.json()
        mock_http_client.post.assert_called_once()

    def test_server_error(self, mock_http_client):
        # Mock error response
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Error",
            request=httpx.Request("POST", "http://test"),
            response=mock_response,
        )
        mock_http_client.post.return_value = mock_response

        # Test data
        test_data = {
            "city": "London",
            "timeOfDay": ["Morning"],
            "group": "Family",
        }

        # Make request
        response = client.post("/activities", json=test_data)

        # Assertions
        assert response.status_code == 500
        mock_http_client.post.assert_called_once()

    def test_invalid_request_data(self):
        # Test data with invalid format
        test_data = {
            "city": 123,  # Should be string
            "timeOfDay": "Morning",  # Should be list
            "group": "Family",
        }

        # Make request
        response = client.post("/activities", json=test_data)

        # Assertions
        assert response.status_code == 422  # Validation error

    def test_missing_required_field(self):
        # Test data missing required field
        test_data = {
            "city": "London",
            # missing timeOfDay
            "group": "Family",
        }

        # Make request
        response = client.post("/activities", json=test_data)

        # Assertions
        assert response.status_code == 422


class TestItineraryEndpoint:
    def test_success(self, mock_http_client):
        # Mock response data
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "itinerary": [
                {
                    "title": "Test Item",
                    "transport": False,
                    "start": "09:00",
                    "end": "10:00",
                    "description": "Test Description",
                    "price": 15.00,
                    "theme": "Adventure",
                    "transportMode": "N/A",
                    "requires_booking": False,
                    "booking_url": "https://example.com/booking",
                    "image": "https://example.com/image.jpg",
                    "duration": 60,
                    "id": 1,
                }
            ]
        }
        mock_http_client.post.return_value = mock_response

        # Test data
        test_data = {
            "city": "London",
            "preferences": [
                {
                    "liked": ["Activity 1", "Activity 2"],
                    "disliked": ["Activity 3"],
                }
            ],
        }

        # Make request
        response = client.post("/itinerary", json=test_data)

        # Assertions
        assert response.status_code == 200
        assert "itinerary" in response.json()
        mock_http_client.post.assert_called_once()

    def test_server_error(self, mock_http_client):
        # Mock error response
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Error",
            request=httpx.Request("POST", "http://test"),
            response=mock_response,
        )
        mock_http_client.post.return_value = mock_response

        # Test data
        test_data = {
            "city": "London",
            "preferences": [
                {
                    "liked": ["Activity 1", "Activity 2"],
                    "disliked": ["Activity 3"],
                }
            ],
        }

        # Make request
        response = client.post("/itinerary", json=test_data)

        # Assertions
        assert response.status_code == 500
        mock_http_client.post.assert_called_once()

    def test_invalid_request_data(self):
        # Test data with invalid format
        test_data = {
            "city": 123,  # Should be string
            "preferences": "not a list",  # Should be list of preferences
        }

        # Make request
        response = client.post("/itinerary", json=test_data)

        # Assertions
        assert response.status_code == 422"""

    def test_missing_required_field(self):
        # Test data missing required field
        test_data = {
            # missing city
            "preferences": [
                {"liked": ["Activity 1"], "disliked": ["Activity 2"]}
            ]
        }

        # Make request
        response = client.post("/itinerary", json=test_data)

        # Assertions
        assert response.status_code == 422
