from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import activities, itinerary, default, saving, map
from config import PORT
from dotenv import load_dotenv


# Load environment variables
load_dotenv(override=True)

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
app.include_router(saving.router)
app.include_router(map.router)
app.include_router(default.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
