"""
Google Calendar integration for adding Mikew's performances
"""
import os
import pickle
import json
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import (
    GOOGLE_CALENDAR_ID, 
    GOOGLE_CREDENTIALS_FILE, 
    GOOGLE_TOKEN_FILE,
    SCRAPE_HISTORY_FILE,
    PERFORMANCES_FILE
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarManager:
    def __init__(self):
        self.calendar_id = GOOGLE_CALENDAR_ID
        self.creds = None
        self.service = None
        self._authenticate()
        
    def _authenticate(self):
        """Authenticate with Google Calendar API"""
        try:
            # The file token.json stores the user's access and refresh tokens.
            if os.path.exists(GOOGLE_TOKEN_FILE):
                self.creds = Credentials.from_authorized_user_file(GOOGLE_TOKEN_FILE, SCOPES)
                
            # If there are no (valid) credentials available, let the user log in.
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    # Check if credentials file exists
                    if not os.path.exists(GOOGLE_CREDENTIALS_FILE):
                        logger.warning(f"Credentials file {GOOGLE_CREDENTIALS_FILE} not found.")
                        logger.info("Please set up Google Calendar API credentials.")
                        return
                        
                    flow = InstalledAppFlow.from_client_secrets_file(
                        GOOGLE_CREDENTIALS_FILE, SCOPES)
                    # For automated systems, we'll need to handle authentication differently
                    # This is just for initial setup
                    logger.info("Manual authentication required for Google Calendar API")
                    return
                    
                # Save the credentials for the next run
                with open(GOOGLE_TOKEN_FILE, 'w') as token:
                    token.write(self.creds.to_json())
                    
            self.service = build('calendar', 'v3', credentials=self.creds)
            logger.info("Successfully authenticated with Google Calendar API")
            
        except Exception as e:
            logger.error(f"Error authenticating with Google Calendar API: {e}")
            
    def create_event(self, performance_data: Dict[str, Any]) -> str:
        """
        Create a calendar event for a performance
        
        Args:
            performance_data: Dictionary containing performance details
            
        Returns:
            Event ID if successful, None otherwise
        """
        if not self.service:
            logger.error("Google Calendar service not initialized")
            return None
            
        try:
            # Create event object
            event = {
                'summary': f"{performance_data.get('busker_name', 'Mikew')} Performance",
                'location': performance_data.get('location', 'TBD'),
                'description': f"Mikew's performance at {performance_data.get('location', 'TBD')}",
                'start': {
                    'dateTime': performance_data.get('start_time', ''),
                    'timeZone': 'Asia/Singapore',
                },
                'end': {
                    'dateTime': performance_data.get('end_time', ''),
                    'timeZone': 'Asia/Singapore',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 30},       # 30 minutes before
                    ],
                },
            }
            
            # Insert the event
            event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
            event_id = event.get('id')
            logger.info(f"Event created: {event_id}")
            return event_id
            
        except HttpError as error:
            logger.error(f"An error occurred creating calendar event: {error}")
            return None
            
    def get_upcoming_events(self, days_ahead: int = 30) -> List[Dict]:
        """
        Get upcoming events from the calendar
        
        Args:
            days_ahead: Number of days to look ahead for events
            
        Returns:
            List of event dictionaries
        """
        if not self.service:
            logger.error("Google Calendar service not initialized")
            return []
            
        try:
            # Get current time and time 'days_ahead' days in the future
            now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            end_time = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + 'Z'
            
            events_result = self.service.events().list(calendarId=self.calendar_id, 
                                                      timeMin=now,
                                                      timeMax=end_time,
                                                      maxResults=50, 
                                                      singleEvents=True,
                                                      orderBy='startTime').execute()
            events = events_result.get('items', [])
            
            return events
            
        except HttpError as error:
            logger.error(f"An error occurred fetching calendar events: {error}")
            return []
            
    def delete_event(self, event_id: str) -> bool:
        """
        Delete a calendar event
        
        Args:
            event_id: ID of the event to delete
            
        Returns:
            True if successful, False otherwise
        """
        if not self.service:
            logger.error("Google Calendar service not initialized")
            return False
            
        try:
            self.service.events().delete(calendarId=self.calendar_id, eventId=event_id).execute()
            logger.info(f"Event deleted: {event_id}")
            return True
            
        except HttpError as error:
            logger.error(f"An error occurred deleting calendar event: {error}")
            return False

# Example usage
if __name__ == "__main__":
    calendar_manager = GoogleCalendarManager()
    
    # Example performance data (would come from scraper in real implementation)
    sample_performance = {
        'busker_name': 'Mikew (FattKew The OneBoyBand)',
        'location': 'Marina Bay Sands',
        'start_time': '2025-12-20T19:00:00',
        'end_time': '2025-12-20T21:00:00'
    }
    
    # Uncomment to test event creation (requires authentication)
    # event_id = calendar_manager.create_event(sample_performance)
    # print(f"Created event with ID: {event_id}")