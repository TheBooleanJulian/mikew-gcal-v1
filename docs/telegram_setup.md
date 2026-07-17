# Telegram Bot Setup

To enable Telegram notifications, you'll need to create a Telegram bot and set up a channel.

## Prerequisites

1. A Telegram account
2. Telegram Desktop or mobile app

## Steps to Set Up Telegram Integration

### 1. Create a Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Start a chat with BotFather by clicking "Start"
3. Send the command `/newbot`
4. Follow the prompts to:
   - Enter a name for your bot (e.g., "Mikew Performance Tracker")
   - Enter a username for your bot (must end in "bot", e.g., "mikew_performance_tracker_bot")
5. BotFather will provide you with a token that looks like `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`
6. Save this token - you'll need it for configuration

### 2. Create a Telegram Channel

1. In Telegram, tap the pencil icon (Android) or compose button (iOS) to create a new chat
2. Select "New Channel"
3. Enter a name (e.g., "Mikew Performances")
4. Add a description if desired
5. Set privacy settings:
   - For private channels: Select "Private" and save the invite link
   - For public channels: Select "Public" and choose a public link
6. Create the channel

### 3. Add Your Bot to the Channel

1. Open your newly created channel
2. Tap the channel name to open channel info
3. Tap "Administrators"
4. Tap "Add Administrator"
5. Search for your bot by username (the one you created with BotFather)
6. Confirm adding the bot as an administrator
7. Ensure the bot has permission to post messages

### 4. Get Your Channel ID

Getting the channel ID depends on whether you created a public or private channel:

#### For Public Channels:
Your channel ID is the username you chose prefixed with "@", e.g., "@mikew_performances"

#### For Private Channels:
1. Forward any message from the channel to [@JsonDumpBot](https://t.me/JsonDumpBot)
2. The bot will reply with JSON data
3. Look for the "chat" object and find the "id" field
4. The ID will be a negative number, e.g., "-1001234567890"

Alternatively, you can use this method:
1. Post a message in your channel
2. Forward that message to [@GetChannelIdBot](https://t.me/GetChannelIdBot)
3. The bot will reply with your channel ID

### 5. Configure the Application

1. Open the `.env` file in your project root
2. Update the following values:
   ```
   TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
   TELEGRAM_CHANNEL_ID=your_channel_id_here
   ```

## Testing the Setup

To test if your Telegram integration is working:

1. Make sure you've updated the `.env` file with your bot token and channel ID
2. Run the test command:
   ```bash
   python src/main.py --test-telegram
   ```
3. Check your Telegram channel for a test message

## Troubleshooting

### Bot Not Sending Messages

1. Verify the bot token is correct
2. Ensure the bot is an administrator in the channel
3. Check that the channel ID is correct
4. Make sure the bot has permission to post messages

### "Forbidden: bot is not a member of the chat" Error

1. Make sure you've added the bot to your channel
2. Confirm the bot is an administrator
3. Double-check the channel ID is correct

### "Unauthorized" Error

1. Verify your bot token is correct
2. If you regenerated the token, make sure to update it in your `.env` file