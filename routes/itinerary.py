from fastapi import APIRouter, HTTPException
import httpx
from models import RateCard
from config import BACKEND_URL, MAX_TIMEOUT

router = APIRouter()


@router.post("/itinerary")
async def itinerary(rate_card_response: RateCard):
    """Handle itinerary endpoint."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BACKEND_URL}/itinerary",
                json=rate_card_response.model_dump(),
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
