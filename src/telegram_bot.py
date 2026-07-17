"""
Telegram bot integration for posting Mikew's performance updates
"""
import logging
from typing import Dict, List
from telegram import Bot
from telegram.error import TelegramError

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.channel_id = TELEGRAM_CHANNEL_ID
        self.bot = None
        
        if self.bot_token and self.channel_id:
            self.bot = Bot(token=self.bot_token)
            logger.info("Telegram bot initialized")
        else:
            logger.warning("Telegram bot not configured - missing token or channel ID")
            
    def format_performance_message(self, performance_data: Dict) -> str:
        """
        Format performance data into a readable message for Telegram
        
        Args:
            performance_data: Dictionary containing performance details
            
        Returns:
            Formatted message string
        """
        # Extract performance details
        busker_name = performance_data.get('busker_name', 'Mikew')
        date = performance_data.get('date', 'TBD')
        start_time = performance_data.get('start_time', 'TBD')
        end_time = performance_data.get('end_time', 'TBD')
        location = performance_data.get('location', 'TBD')
        
        # Format message
        message = f"🎵 *NEW PERFORMANCE ALERT* 🎵\n\n"
        message += f"**Artist:** {busker_name}\n"
        message += f"**Date:** {date}\n"
        message += f"**Time:** {start_time} - {end_time}\n"
        message += f"**Location:** {location}\n\n"
        message += "Come enjoy some amazing music! 🎤🎸"
        
        return message
        
    def send_performance_update(self, performance_data: Dict) -> bool:
        """
        Send a performance update to the Telegram channel
        
        Args:
            performance_data: Dictionary containing performance details
            
        Returns:
            True if successful, False otherwise
        """
        if not self.bot:
            logger.error("Telegram bot not initialized")
            return False
            
        try:
            # Format the message
            message = self.format_performance_message(performance_data)
            
            # Send message to channel
            self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode='Markdown'
            )
            
            logger.info("Performance update sent to Telegram channel")
            return True
            
        except TelegramError as e:
            logger.error(f"Error sending message to Telegram: {e}")
            return False
            
    def send_daily_summary(self, performances: List[Dict]) -> bool:
        """
        Send a daily summary of all upcoming performances
        
        Args:
            performances: List of performance dictionaries
            
        Returns:
            True if successful, False otherwise
        """
        if not self.bot:
            logger.error("Telegram bot not initialized")
            return False
            
        if not performances:
            message = "📅 *Daily Performance Summary*\n\n"
            message += "No upcoming performances scheduled for today."
        else:
            message = "📅 *Daily Performance Summary*\n\n"
            message += f"Found {len(performances)} upcoming performance(s):\n\n"
            
            for i, perf in enumerate(performances, 1):
                date = perf.get('date', 'TBD')
                start_time = perf.get('start_time', 'TBD')
                location = perf.get('location', 'TBD')
                
                message += f"{i}. *{date}* at {start_time}\n"
                message += f"   Location: {location}\n\n"
                
        try:
            self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode='Markdown'
            )
            
            logger.info("Daily summary sent to Telegram channel")
            return True
            
        except TelegramError as e:
            logger.error(f"Error sending daily summary to Telegram: {e}")
            return False

# Example usage
if __name__ == "__main__":
    notifier = TelegramNotifier()
    
    # Sample performance data
    sample_performance = {
        'busker_name': 'Mikew (FattKew The OneBoyBand)',
        'date': '20 Dec 2025',
        'start_time': '7:00 PM',
        'end_time': '9:00 PM',
        'location': 'Marina Bay Sands'
    }
    
    # Uncomment to test sending a message (requires valid bot token and channel ID)
    # notifier.send_performance_update(sample_performance)