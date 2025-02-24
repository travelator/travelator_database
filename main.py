from fastapi import FastAPI, HTTPException
import httpx
from fastapi.middleware.cors import CORSMiddleware
from models import ActivityRequest, RateCard

app = FastAPI()

origins = [
    "http://localhost:8080",  # React development server
    "http://localhost",  # React dev server if running directly via `localhost`
    # Add your production frontend URL here when deployed
    "https://voya/trips.com",  # frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[
        "*"
    ],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

BACKEND_URL = "https://your-backend-service.com/api"

http_client = httpx.AsyncClient()


@app.post("/activities")
async def activities(initial_parameters: ActivityRequest):
    try:
        response = await http_client.post(
            f"{BACKEND_URL}/activities", json=initial_parameters.model_dump()
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/itinerary")
async def itinerary(rate_card_response: RateCard):
    try:
        response = await http_client.post(
            f"{BACKEND_URL}/itinerary", json=rate_card_response.model_dump()
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
