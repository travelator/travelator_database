from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import activities, itinerary, default
from dotenv import load_dotenv
import os
from map import get_google_directions, DirectionsRequest

# Load environment variables
load_dotenv()

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL")
PORT = int(os.getenv("PORT", "5000"))

# Create FastAPI app
app = FastAPI(title="Travelator Database API")

# Configure CORS
origins = [
    "http://localhost:8080",  # React development server
    "http://localhost",  # React dev server if running directly via `localhost`
    "https://voya-trips.com",  # frontend
    "https://www.voya-trips.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(activities.router)
app.include_router(itinerary.router)


@app.post("/get-directions")
async def get_directions(request: DirectionsRequest):
    route_data = get_google_directions(
        request.origin, request.destination, request.mode
    )
    if not route_data:
        return {"error": "No route found"}

    return {"routes": route_data}


app.include_router(default.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
