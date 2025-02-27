"""Configuration for the Travelator Database API."""

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API Configuration
BACKEND_URL = os.getenv("BACKEND_URL")
PORT = int(os.getenv("PORT", "5000"))
MAX_TIMEOUT = 120
