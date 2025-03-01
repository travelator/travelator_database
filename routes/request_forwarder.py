from fastapi import Request, Response
import json
import httpx

MAX_TIMEOUT = 120


async def forward_request(request: Request, method: str, url: str) -> Response:
    """Forward a request with its body, headers, cookies, and query parameters to another service."""
    body = await request.body()
    try:
        json_body = json.loads(body)
    except:
        json_body = None

    query_params = request.query_params

    async with httpx.AsyncClient() as client:
        cookies = request.cookies
        response = await client.request(
            method=method,
            url=url,
            json=json_body,
            cookies=cookies,
            params=query_params,
            timeout=MAX_TIMEOUT,
        )
        response.raise_for_status()

        # Return response with cookies from the backend if needed
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=response.headers,
        )
