from fastapi import APIRouter, Request
from config import BACKEND_URL
from .request_forwarder import forward_request

router = APIRouter()


@router.post("/activities")
async def activities(request: Request):
    """Handle activities endpoint."""
    return await forward_request(
        request=request,
        method="post",
        url=f"{BACKEND_URL}/activities",
    )
