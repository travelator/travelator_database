from fastapi import Request, Response
import httpx
MAX_TIMEOUT = 120


async def forward_request(request: Request, method: str, url: str) -> Response:
    """Forward a request with its body, headers, and cookies to another service."""
    async with httpx.AsyncClient() as client:
        cookies = request.cookies
        response = await client.request(
            method=method,
            url=url,
            json=await request.json(),
            cookies=cookies,
            timeout=MAX_TIMEOUT,
        )
        response.raise_for_status()

        # Return response with cookies from the backend if needed
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=response.headers,
        )
