<div align="center">

# Mikew's Performance Schedule Tracker

**Automatically scrapes Mikew's busking schedule and syncs it to Google Calendar with Telegram notifications.**

![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-00D4C8.svg)

</div>

---

## What it does

Scrapes performance listings for Mikew (FattKew The OneBoyBand) from the NAC Busking website and keeps a Google Calendar up to date automatically. New or changed performances trigger a Telegram channel notification, and the whole cycle repeats on a configurable daily schedule — so anyone following the channel always knows where Mikew is performing next without manual updates.

## Features

- Daily scraping of the NAC Busking performance schedule
- Automatic creation/update of events in Google Calendar
- Telegram channel notifications for new performances
- Persistent local storage of scraped data and scrape history
- One-shot (`--once`) and continuous scheduling modes
- Integration test flags for Telegram and Calendar without a full run

## Tech Stack

| Layer | Choice |
|---|---|
| Scraper | Python + Requests + BeautifulSoup4 |
| Calendar | Google Calendar API (google-api-python-client + google-auth) |
| Bot | python-telegram-bot 20.6 |
| Scheduling | schedule |
| Config | python-dotenv |

## Quick Start

```bash
git clone https://github.com/TheBooleanJulian/mikew-gcal-v1
cd mikew-gcal-v1
python setup.py          # installs packages, creates data/ and .env template
cp .env .env.local       # edit with your credentials (see Configuration)
python src/main.py       # run continuously (daily refresh)
```

Run once and exit:

```bash
python src/main.py --once
```

Test integrations without a full scrape run:

```bash
python src/main.py --test-telegram
python src/main.py --test-calendar
```

## Configuration

| Variable | Required | Description |
|---|---|---|
| `GOOGLE_CALENDAR_ID` | Yes | Target calendar ID (e.g. `primary`) |
| `GOOGLE_CREDENTIALS_FILE` | Yes | Path to Google OAuth credentials JSON |
| `GOOGLE_TOKEN_FILE` | Yes | Path where the OAuth token is stored after first auth |
| `TELEGRAM_BOT_TOKEN` | Yes | Bot token from @BotFather |
| `TELEGRAM_CHANNEL_ID` | Yes | Channel ID to post notifications to |
| `REFRESH_INTERVAL_HOURS` | No | How often to re-scrape (default: `24`) |

Full setup guides:
- Google Calendar: [`docs/google_calendar_setup.md`](docs/google_calendar_setup.md)
- Telegram: [`docs/telegram_setup.md`](docs/telegram_setup.md)

## Project Structure

```
mikew-gcal-v1/
|-- src/
|   `-- main.py
|-- data/
|   |-- performances.json
|   `-- scrape_history.json
|-- docs/
|   |-- google_calendar_setup.md
|   `-- telegram_setup.md
|-- setup.py
|-- requirements.txt
`-- .env
```

## Status / Roadmap

- [x] NAC Busking website scraper
- [x] Google Calendar sync
- [x] Telegram channel notifications
- [x] Daily scheduled refresh
- [ ] Detect cancelled/removed performances and remove Calendar events
- [ ] Web dashboard for scrape history

## Changelog

- **2026-07-17** — Initial release: scraper, Google Calendar integration, Telegram notifications, scheduling, and setup script.

## License

MIT

---

<div align="center">
<sub>Built by <a href="https://github.com/TheBooleanJulian">@TheBooleanJulian</a></sub>
</div>