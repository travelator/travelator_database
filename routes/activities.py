from fastapi import APIRouter, HTTPException
import httpx
from models import ActivityRequest
from config import BACKEND_URL, MAX_TIMEOUT

router = APIRouter()


@router.post("/activities")
async def activities(initial_parameters: ActivityRequest):
    """Handle activities endpoint."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BACKEND_URL}/activities",
                json=initial_parameters.model_dump(),
                timeout=MAX_TIMEOUT,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail=e.response.text
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
