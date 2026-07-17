"""
Main application entry point for Mikew's performance tracker
"""
import argparse
import logging
from scheduler import PerformanceScheduler

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Mikew's Performance Tracker")
    parser.add_argument('--once', action='store_true', 
                       help='Run the scraper once and exit (instead of running continuously)')
    parser.add_argument('--test-telegram', action='store_true',
                       help='Test Telegram notification')
    parser.add_argument('--test-calendar', action='store_true',
                       help='Test Google Calendar integration')
    
    args = parser.parse_args()
    
    scheduler = PerformanceScheduler()
    
    if args.test_telegram:
        logger.info("Testing Telegram notification...")
        # Import here to avoid circular imports
        from telegram_bot import TelegramNotifier
        notifier = TelegramNotifier()
        
        # Sample performance data for testing
        sample_performance = {
            'busker_name': 'Mikew (FattKew The OneBoyBand)',
            'date': '20 Dec 2025',
            'start_time': '7:00 PM',
            'end_time': '9:00 PM',
            'location': 'Marina Bay Sands'
        }
        
        success = notifier.send_performance_update(sample_performance)
        if success:
            print("Telegram test message sent successfully!")
        else:
            print("Failed to send Telegram test message.")
        return
        
    if args.test_calendar:
        logger.info("Testing Google Calendar integration...")
        # Import here to avoid circular imports
        from calendar_integration import GoogleCalendarManager
        calendar_manager = GoogleCalendarManager()
        
        # Sample performance data for testing
        sample_performance = {
            'busker_name': 'Mikew (FattKew The OneBoyBand)',
            'location': 'Marina Bay Sands',
            'start_time': '2025-12-20T19:00:00',
            'end_time': '2025-12-20T21:00:00'
        }
        
        event_id = calendar_manager.create_event(sample_performance)
        if event_id:
            print(f"Calendar test event created successfully with ID: {event_id}")
        else:
            print("Failed to create calendar test event.")
        return
        
    if args.once:
        logger.info("Running performance tracker once...")
        scheduler.run_once()
    else:
        logger.info("Starting performance tracker scheduler...")
        scheduler.start_scheduler()

if __name__ == "__main__":
    main()