import pytest
from fastapi import Request
from unittest.mock import AsyncMock, patch
import json

# Import the function to test
from routes.request_forwarder import forward_request, MAX_TIMEOUT


@pytest.mark.asyncio
async def test_forward_request_with_json_body():
    # Create a mock request with JSON body
    mock_request = AsyncMock(spec=Request)
    mock_request.body.return_value = json.dumps({"key": "value"}).encode()
    mock_request.query_params = {}
    mock_request.cookies = {}

    # Target URL to forward request
    target_url = "http://example.com/endpoint"
    method = "POST"

    # Mock the httpx.AsyncClient to simulate a successful response
    with patch("httpx.AsyncClient") as mock_client:
        # Create a mock response
        mock_response = AsyncMock()
        mock_response.content = b"Success response"
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.raise_for_status = AsyncMock()

        # Configure the mock client to return the mock response
        mock_client_instance = AsyncMock()
        mock_client_instance.request.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        # Call the function
        response = await forward_request(mock_request, method, target_url)

        # Assertions
        assert response.status_code == 200
        assert (
            response.body == b"Success response"
        )  # Use `body` instead of `content`

        # Verify that the client.request was called with correct parameters
        mock_client_instance.request.assert_called_once_with(
            method=method,
            url=target_url,
            json={"key": "value"},
            cookies={},
            params={},
            timeout=MAX_TIMEOUT,
        )


@pytest.mark.asyncio
async def test_forward_request_with_invalid_json_body():
    # Create a mock request with invalid JSON body
    mock_request = AsyncMock(spec=Request)
    mock_request.body.return_value = b"Invalid JSON"
    mock_request.query_params = {}
    mock_request.cookies = {}

    # Target URL to forward request
    target_url = "http://example.com/endpoint"
    method = "POST"

    # Mock the httpx.AsyncClient to simulate a successful response
    with patch("httpx.AsyncClient") as mock_client:
        # Create a mock response
        mock_response = AsyncMock()
        mock_response.content = b"Success response"
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.raise_for_status = AsyncMock()

        # Configure the mock client to return the mock response
        mock_client_instance = AsyncMock()
        mock_client_instance.request.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        # Call the function
        response = await forward_request(mock_request, method, target_url)

        # Assertions
        assert response.status_code == 200
        assert (
            response.body == b"Success response"
        )  # Use `body` instead of `content`

        # Verify that the client.request was called with correct parameters
        mock_client_instance.request.assert_called_once_with(
            method=method,
            url=target_url,
            json=None,
            cookies={},
            params={},
            timeout=MAX_TIMEOUT,
        )
