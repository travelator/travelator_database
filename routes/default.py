from fastapi import APIRouter, Request, HTTPException
from config import BACKEND_URL
from .request_forwarder import forward_request

router = APIRouter()


@router.api_route(
    "/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"]
)
async def catch_all(request: Request, path_name: str):
    """Catch all route that forwards the request."""
    # Exclude /get-directions from being forwarded
    if path_name == "get-directions":
        raise HTTPException(status_code=404, detail="Not Found")

    url = f"{BACKEND_URL}/{path_name}"
    return await forward_request(
        request=request,
        method=request.method.lower(),
        url=url,
    )
