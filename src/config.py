"""
Configuration file for the Mikew performance tracker
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Busker information
BUSKER_ID = "dbc5b6bc-e22a-4e60-9fe4-f4d6a1aa17a4"
BUSKER_NAME = "Mikew (FattKew The OneBoyBand)"

# NAC Busking website
NAC_BASE_URL = "https://eservices.nac.gov.sg/Busking/busker/profile/"

# Google Calendar settings
GOOGLE_CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID", "fec731e846c5f2bf53f17ade0152aa8fe1197c79fcbcc470460b6fc2f8106701@group.calendar.google.com")
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
GOOGLE_TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE", "token.json")

# Telegram settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")

# Scheduling
REFRESH_INTERVAL_HOURS = int(os.getenv("REFRESH_INTERVAL_HOURS", "24"))

# File paths for storing data
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

SCRAPE_HISTORY_FILE = os.path.join(DATA_DIR, "scrape_history.json")
PERFORMANCES_FILE = os.path.join(DATA_DIR, "performances.json")