# Mikew's Performance Schedule Tracker

This project automatically scrapes performance information for Mikew (FattKew The OneBoyBand) from the NAC Busking website and integrates with Google Calendar and Telegram.

## Features
- Daily scraping of performance schedule
- Automatic updates to Google Calendar
- Notifications posted to Telegram channel
- Scheduled daily refresh

## Prerequisites

- Python 3.7 or higher
- A Google account for Google Calendar integration
- A Telegram account for Telegram notifications

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Run the setup script:
   ```bash
   python setup.py
   ```
   This will:
   - Install required Python packages
   - Create a data directory for storing scraped information
   - Create a template `.env` configuration file

## Configuration

### 1. Google Calendar Setup

Follow the instructions in [docs/google_calendar_setup.md](docs/google_calendar_setup.md) to set up Google Calendar integration.

### 2. Telegram Setup

Follow the instructions in [docs/telegram_setup.md](docs/telegram_setup.md) to set up Telegram notifications.

### 3. Environment Variables

Update the `.env` file with your configuration:

```env
# Google Calendar Configuration
GOOGLE_CALENDAR_ID=primary
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_TOKEN_FILE=token.json

# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHANNEL_ID=your_channel_id_here

# Scheduling
REFRESH_INTERVAL_HOURS=24
```

## Usage

### Run Once

To run the scraper once and exit:
```bash
python src/main.py --once
```

### Continuous Operation

To run the scraper continuously with daily refresh:
```bash
python src/main.py
```

### Test Integrations

To test Telegram integration:
```bash
python src/main.py --test-telegram
```

To test Google Calendar integration:
```bash
python src/main.py --test-calendar
```

## How It Works

1. The scraper extracts performance information from the NAC Busking website
2. New performances are added to Google Calendar
3. Notifications are sent to the Telegram channel
4. The process repeats daily according to the configured interval

## Data Storage

- `data/performances.json`: Stores the most recent scraped performance data
- `data/scrape_history.json`: Tracks scraping history and results
- `token.json`: Google Calendar API authentication token (created after first authentication)

## Troubleshooting

See the troubleshooting sections in the Google Calendar and Telegram setup documents for common issues.