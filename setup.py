"""
Setup script for Mikew's Performance Tracker
"""
import os
import sys
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def install_requirements():
    """Install required packages from requirements.txt"""
    logger.info("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("Required packages installed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing packages: {e}")
        return False
    return True

def create_env_file():
    """Create a template .env file for configuration"""
    env_content = """# Google Calendar Configuration
GOOGLE_CALENDAR_ID=primary
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_TOKEN_FILE=token.json

# Telegram Configuration
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHANNEL_ID=

# Scheduling
REFRESH_INTERVAL_HOURS=24
"""
    
    env_file_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(env_file_path):
        try:
            with open(env_file_path, "w") as f:
                f.write(env_content)
            logger.info(".env file created successfully")
            return True
        except Exception as e:
            logger.error(f"Error creating .env file: {e}")
            return False
    else:
        logger.info(".env file already exists")
        return True

def create_data_directory():
    """Create data directory for storing scraped data"""
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    try:
        os.makedirs(data_dir, exist_ok=True)
        logger.info("Data directory created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating data directory: {e}")
        return False

def main():
    """Main setup function"""
    logger.info("Setting up Mikew's Performance Tracker...")
    
    # Create data directory
    if not create_data_directory():
        logger.error("Failed to create data directory")
        return False
    
    # Create .env file
    if not create_env_file():
        logger.error("Failed to create .env file")
        return False
    
    # Install requirements
    if not install_requirements():
        logger.error("Failed to install requirements")
        return False
    
    logger.info("Setup completed successfully!")
    logger.info("Next steps:")
    logger.info("1. Configure your Google Calendar API credentials")
    logger.info("2. Set up your Telegram bot token and channel ID in .env")
    logger.info("3. Run 'python src/main.py' to start the application")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)