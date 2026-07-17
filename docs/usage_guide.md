# Usage Guide

This guide explains how to use the Mikew Performance Tracker to automatically scrape performance information and integrate with Google Calendar and Telegram.

## System Overview

The Mikew Performance Tracker is designed to:
1. Automatically scrape performance schedule information from the NAC Busking website
2. Add new performances to Google Calendar
3. Send notifications to a Telegram channel
4. Run on a daily schedule to keep information up-to-date

## Initial Setup

Before running the system for the first time, you must complete the following setup steps:

### 1. Install Dependencies

Run the setup script to install all required packages:
```bash
python setup.py
```

### 2. Configure Google Calendar Integration

Follow the instructions in [google_calendar_setup.md](google_calendar_setup.md) to:
- Create a Google Cloud project
- Enable the Calendar API
- Create OAuth credentials
- Download the credentials file

Place the downloaded `credentials.json` file in your project root directory.

### 3. Configure Telegram Integration

Follow the instructions in [telegram_setup.md](telegram_setup.md) to:
- Create a Telegram bot
- Create a Telegram channel
- Add your bot to the channel
- Obtain your bot token and channel ID

Update the `.env` file with your Telegram configuration:
```env
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
TELEGRAM_CHANNEL_ID=your_channel_id_here
```

## Running the Application

### First Run

On the first run, you'll need to authenticate with Google Calendar:

1. Run the application:
   ```bash
   python src/main.py --once
   ```

2. A browser window will open asking you to sign in to your Google account
3. Select the account you want to use
4. Review the permissions and click "Allow"
5. The application will save a `token.json` file for future use

### Normal Operation

After the initial setup, you can run the application in continuous mode:
```bash
python src/main.py
```

This will:
1. Run an immediate refresh of performance data
2. Schedule daily refreshes according to the configured interval (default: every 24 hours)

### Run Once Mode

To run the scraper once and exit (useful for testing or manual runs):
```bash
python src/main.py --once
```

### Testing Integrations

You can test individual integrations without scraping data:

Test Telegram integration:
```bash
python src/main.py --test-telegram
```

Test Google Calendar integration:
```bash
python src/main.py --test-calendar
```

## Configuration Options

The system can be configured through the `.env` file:

```env
# Google Calendar Configuration
GOOGLE_CALENDAR_ID=primary              # Calendar to add events to
GOOGLE_CREDENTIALS_FILE=credentials.json # Google API credentials file
GOOGLE_TOKEN_FILE=token.json            # Authentication token file

# Telegram Configuration
TELEGRAM_BOT_TOKEN=                     # Your Telegram bot token
TELEGRAM_CHANNEL_ID=                    # Your Telegram channel ID

# Scheduling
REFRESH_INTERVAL_HOURS=24               # How often to check for new performances
```

## Data Files

The system creates and uses several data files:

- `data/performances.json`: Contains the most recent scraped performance data
- `data/scrape_history.json`: Tracks when scrapes were performed and their results
- `token.json`: Google Calendar API authentication token (created after first authentication)

These files are automatically managed by the system. You typically don't need to modify them manually.

## Monitoring and Troubleshooting

### Log Output

The application outputs logs to the console showing:
- When scraping starts and completes
- Whether new performances were found
- Any errors that occur
- When calendar events are created
- When Telegram messages are sent

### Common Issues

1. **Authentication errors with Google Calendar**
   - Solution: Delete `token.json` and re-authenticate

2. **Telegram messages not sending**
   - Verify bot token and channel ID are correct
   - Ensure bot is added as administrator to the channel
   - Check that the bot has permission to post messages

3. **No new performances detected**
   - Check the NAC Busking website to verify there are upcoming performances
   - The scraper may need updates if the website structure changes

### Manual Data Management

If you need to reset the system:
1. Delete `data/performances.json` to clear stored performance data
2. Delete `data/scrape_history.json` to clear scraping history
3. Delete `token.json` to force re-authentication with Google Calendar

## Customization

### Modifying the Scraper

The web scraper is located in `src/scraper.py`. If the NAC Busking website structure changes, you may need to update:
- The URL parsing logic
- The performance data extraction methods
- The selectors used to find performance information

### Modifying Notification Format

The Telegram notification format can be customized in `src/telegram_bot.py`:
- Modify `format_performance_message()` to change individual performance notifications
- Modify `send_daily_summary()` to change the daily summary format

### Changing Schedule Frequency

Adjust the refresh interval by modifying `REFRESH_INTERVAL_HOURS` in the `.env` file or by changing the default value in `src/config.py`.

## Limitations and Future Improvements

### Current Limitations

1. The scraper currently only identifies that performances exist but doesn't extract specific dates, times, and locations due to the structure of the NAC website
2. The system assumes all scraped performances are new (no deduplication)
3. Error handling could be enhanced for network issues

### Potential Enhancements

1. Improve the scraper to extract detailed performance information
2. Add deduplication logic to prevent duplicate calendar events
3. Add email notifications as an additional notification method
4. Create a web dashboard to visualize upcoming performances
5. Add support for multiple buskers
6. Implement more sophisticated error handling and retry logic