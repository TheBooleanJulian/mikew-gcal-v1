"""
Scheduler for daily refresh of Mikew's performance data
"""
import schedule
import time
import logging
from datetime import datetime
import json
import os

from config import REFRESH_INTERVAL_HOURS, SCRAPE_HISTORY_FILE, PERFORMANCES_FILE
from scraper import NACBuskingScraper
from calendar_integration import GoogleCalendarManager
from telegram_bot import TelegramNotifier

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceScheduler:
    def __init__(self):
        self.scraper = NACBuskingScraper("dbc5b6bc-e22a-4e60-9fe4-f4d6a1aa17a4")
        self.calendar_manager = GoogleCalendarManager()
        self.telegram_notifier = TelegramNotifier()
        
    def load_previous_performances(self) -> dict:
        """
        Load previously scraped performances from file
        
        Returns:
            Dictionary of previous performances
        """
        if os.path.exists(PERFORMANCES_FILE):
            try:
                with open(PERFORMANCES_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading previous performances: {e}")
                return {}
        return {}
        
    def save_performances(self, performances: dict):
        """
        Save performances to file
        
        Args:
            performances: Dictionary of performances to save
        """
        try:
            with open(PERFORMANCES_FILE, 'w') as f:
                json.dump(performances, f, indent=2)
            logger.info("Performances saved to file")
        except Exception as e:
            logger.error(f"Error saving performances: {e}")
            
    def load_scrape_history(self) -> dict:
        """
        Load scrape history from file
        
        Returns:
            Dictionary of scrape history
        """
        if os.path.exists(SCRAPE_HISTORY_FILE):
            try:
                with open(SCRAPE_HISTORY_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading scrape history: {e}")
                return {}
        return {}
        
    def save_scrape_history(self, history: dict):
        """
        Save scrape history to file
        
        Args:
            history: Dictionary of scrape history to save
        """
        try:
            with open(SCRAPE_HISTORY_FILE, 'w') as f:
                json.dump(history, f, indent=2)
            logger.info("Scrape history saved to file")
        except Exception as e:
            logger.error(f"Error saving scrape history: {e}")
            
    def compare_performances(self, previous: dict, current: dict) -> dict:
        """
        Compare previous and current performances to find new or changed events
        
        Args:
            previous: Previous performances dictionary
            current: Current performances dictionary
            
        Returns:
            Dictionary containing new and updated performances
        """
        new_performances = []
        updated_performances = []
        
        # For now, we'll just return all current performances as "new"
        # In a real implementation, we'd compare based on unique identifiers
        current_performances = current.get('performances', [])
        
        # Simple approach: treat all current performances as new
        # A more sophisticated approach would compare with previous data
        return {
            'new': current_performances,
            'updated': [],
            'removed': []
        }
        
    def update_calendar_and_telegram(self, new_performances: list):
        """
        Update Google Calendar and Telegram with new performances
        
        Args:
            new_performances: List of new performance dictionaries
        """
        for performance in new_performances:
            # Add to Google Calendar
            event_id = self.calendar_manager.create_event(performance)
            if event_id:
                logger.info(f"Added performance to calendar: {event_id}")
            
            # Send Telegram notification
            success = self.telegram_notifier.send_performance_update(performance)
            if success:
                logger.info("Sent Telegram notification for performance")
                
    def daily_refresh_job(self):
        """
        Main job that runs daily to refresh performance data
        """
        logger.info("Starting daily refresh job")
        
        # Record start time
        start_time = datetime.now().isoformat()
        
        # Load previous data
        previous_performances = self.load_previous_performances()
        scrape_history = self.load_scrape_history()
        
        # Scrape current data
        current_data = self.scraper.run_scraper()
        
        if not current_data:
            logger.error("Failed to scrape current performance data")
            return
            
        # Save current data
        self.save_performances(current_data)
        
        # Compare with previous data
        comparison = self.compare_performances(previous_performances, current_data)
        
        # Handle new performances
        if comparison['new']:
            logger.info(f"Found {len(comparison['new'])} new performances")
            self.update_calendar_and_telegram(comparison['new'])
        else:
            logger.info("No new performances found")
            
        # Update scrape history
        scrape_history[start_time] = {
            'timestamp': start_time,
            'new_performances': len(comparison['new']),
            'updated_performances': len(comparison['updated']),
            'success': True
        }
        self.save_scrape_history(scrape_history)
        
        # Send daily summary to Telegram
        self.telegram_notifier.send_daily_summary(comparison['new'])
        
        logger.info("Daily refresh job completed")
        
    def start_scheduler(self):
        """
        Start the scheduler to run daily refresh jobs
        """
        # Schedule the job to run every REFRESH_INTERVAL_HOURS hours
        schedule.every(REFRESH_INTERVAL_HOURS).hours.do(self.daily_refresh_job)
        
        # Also run once immediately
        logger.info("Running initial refresh job")
        self.daily_refresh_job()
        
        logger.info(f"Scheduler started. Refresh interval: {REFRESH_INTERVAL_HOURS} hours")
        
        # Keep the scheduler running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    def run_once(self):
        """
        Run the refresh job once (for testing purposes)
        """
        self.daily_refresh_job()

# Example usage
if __name__ == "__main__":
    scheduler = PerformanceScheduler()
    
    # For testing, run once
    # scheduler.run_once()
    
    # For production, start the scheduler
    # scheduler.start_scheduler()