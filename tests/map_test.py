import pytest
from unittest.mock import patch, MagicMock
import os
from fastapi.testclient import TestClient

# Import the router to test
from routes.map import router, get_google_directions

# Create a test client
client = TestClient(router)

# Sample test data
MOCK_ORIGIN = [40.7128, -74.0060]  # New York City coordinates
MOCK_DESTINATION = [37.7749, -122.4194]  # San Francisco coordinates
MOCK_MODE = "transit"

# Mock response from Google Directions API
MOCK_DIRECTIONS_RESPONSE = {
    "status": "OK",
    "routes": [
        {
            "legs": [
                {
                    "distance": {"text": "4,677 km", "value": 4677000},
                    "duration": {"text": "3 days 10 hours", "value": 302400},
                    "steps": [
                        {
                            "transit_details": {
                                "line": {
                                    "short_name": "A",
                                    "vehicle": {"type": "SUBWAY"}
                                },
                                "departure_time": {"text": "10:30 AM"}
                            }
                        }
                    ]
                }
            ],
            "overview_polyline": {
                "points": "_p~iF~ps|U_ulLnnqC_mqNvxq`@"  # Sample encoded polyline
            },
            "summary": "I-80 W"
        }
    ]
}

# Expected decoded polyline result for our mock data
EXPECTED_DECODED_POLYLINE = [(38.5, -120.2), (40.7, -120.95), (43.252, -126.453)]


@pytest.fixture
def mock_env_api_key(monkeypatch):
    """Fixture to mock the Google Maps API key environment variable"""
    monkeypatch.setenv("GOOGLE_MAPS_API_KEY", "test_api_key")


def test_get_google_directions_success(mock_env_api_key):
    # Configure the mock to return a successful response
    with patch('routes.map.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = MOCK_DIRECTIONS_RESPONSE
        mock_get.return_value = mock_response

        # Call the function under test
        with patch('routes.map.polyline.decode', return_value=EXPECTED_DECODED_POLYLINE):
            result = get_google_directions(MOCK_ORIGIN, MOCK_DESTINATION, MOCK_MODE)

        # Assertions to verify the function behaves as expected
        assert mock_get.called
        assert result is not None
        assert len(result) == 1
        assert result[0]['polyline'] == EXPECTED_DECODED_POLYLINE
        assert result[0]['duration'] == "3 days 10 hours"
        assert result[0]['summary'] == "I-80 W"
        assert result[0]['distance_km'] == 4677.0
        assert len(result[0]['transit_steps']) == 1
        assert result[0]['transit_steps'][0]['line'] == "A"
        assert result[0]['transit_steps'][0]['type'] == "SUBWAY"
        assert result[0]['transit_steps'][0]['departure'] == "10:30 AM"


def test_get_google_directions_api_error(mock_env_api_key):
    # Configure the mock to return an error response
    with patch('routes.map.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "ZERO_RESULTS"}
        mock_get.return_value = mock_response

        # Call the function under test
        result = get_google_directions(MOCK_ORIGIN, MOCK_DESTINATION, MOCK_MODE)

        # Assertions to verify the function behaves as expected with an error
        assert mock_get.called
        assert result is None


def test_get_google_directions_exception(mock_env_api_key):
    # Configure the mock to raise an exception
    with patch('routes.map.requests.get') as mock_get:
        mock_get.side_effect = Exception("API connection error")

        # Call the function under test
        result = get_google_directions(MOCK_ORIGIN, MOCK_DESTINATION, MOCK_MODE)

        # Assertions to verify the function handles exceptions
        assert mock_get.called
        assert result is None

def test_get_directions_success():
    # Configure the mock to return a successful response
    with patch('routes.map.get_google_directions') as mock_get_google_directions:
        mock_route_data = [
            {
                "polyline": [[38.5, -120.2], [40.7, -120.95], [43.252, -126.453]],  # Changed from tuples to lists
                "duration": "3 days 10 hours",
                "summary": "I-80 W",
                "distance_km": 4677.0,
                "transit_steps": [
                    {
                        "line": "A",
                        "type": "SUBWAY",
                        "departure": "10:30 AM"
                    }
                ]
            }
        ]
        mock_get_google_directions.return_value = mock_route_data

        # Create test request data
        test_data = {
            "origin": MOCK_ORIGIN,
            "destination": MOCK_DESTINATION,
            "mode": MOCK_MODE
        }

        # Send a request to the API endpoint
        response = client.post("/get-directions", json=test_data)

        # Assertions to verify the API response
        assert response.status_code == 200
        assert response.json() == {"routes": mock_route_data}
        mock_get_google_directions.assert_called_once_with(
            MOCK_ORIGIN, MOCK_DESTINATION, MOCK_MODE
        )


def test_get_directions_no_route():
    # Configure the mock to return None (no route found)
    with patch('routes.map.get_google_directions') as mock_get_google_directions:
        mock_get_google_directions.return_value = None

        # Create test request data
        test_data = {
            "origin": MOCK_ORIGIN,
            "destination": MOCK_DESTINATION,
            "mode": MOCK_MODE
        }

        # Send a request to the API endpoint
        response = client.post("/get-directions", json=test_data)

        # Assertions to verify the API response when no route is found
        assert response.status_code == 200
        assert response.json() == {"error": "No route found"}
        mock_get_google_directions.assert_called_once_with(
            MOCK_ORIGIN, MOCK_DESTINATION, MOCK_MODE
        )


# Test different travel modes individually instead of using parametrize
def test_driving_mode(mock_env_api_key):
    with patch('routes.map.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = MOCK_DIRECTIONS_RESPONSE
        mock_get.return_value = mock_response

        with patch('routes.map.polyline.decode', return_value=EXPECTED_DECODED_POLYLINE):
            result = get_google_directions(MOCK_ORIGIN, MOCK_DESTINATION, "driving")

        assert mock_get.called
        call_args = mock_get.call_args[1]['params']
        assert call_args['mode'] == "driving"
        assert result is not None


def test_walking_mode(mock_env_api_key):
    with patch('routes.map.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = MOCK_DIRECTIONS_RESPONSE
        mock_get.return_value = mock_response

        with patch('routes.map.polyline.decode', return_value=EXPECTED_DECODED_POLYLINE):
            result = get_google_directions(MOCK_ORIGIN, MOCK_DESTINATION, "walking")

        assert mock_get.called
        call_args = mock_get.call_args[1]['params']
        assert call_args['mode'] == "walking"
        assert result is not None


def test_missing_api_key():
    # Create a test environment without the API key
    with patch.dict(os.environ, {}, clear=True):
        with patch('routes.map.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = MOCK_DIRECTIONS_RESPONSE
            mock_get.return_value = mock_response

            # Call the function under test
            get_google_directions(MOCK_ORIGIN, MOCK_DESTINATION)

            # The function should still make the API call, but with a None API key
            assert mock_get.called
            call_args = mock_get.call_args[1]['params']
            assert 'key' in call_args