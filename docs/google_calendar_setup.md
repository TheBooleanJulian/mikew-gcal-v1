# Google Calendar API Setup

To enable the Google Calendar integration, you'll need to set up API credentials with Google.

## Prerequisites

1. A Google account
2. Access to Google Cloud Console

## Steps to Set Up Google Calendar API

### 1. Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" then "New Project"
3. Enter a project name (e.g., "Mikew Performance Tracker")
4. Click "Create"

### 2. Enable the Calendar API

1. In the Google Cloud Console, with your project selected, go to "APIs & Services" > "Library"
2. Search for "Google Calendar API"
3. Click on "Google Calendar API" in the results
4. Click "Enable"

### 3. Create Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted to configure the OAuth consent screen:
   - Choose "External" for user type
   - Fill in the required fields (app name, user support email, developer contact information)
   - Add the scope: `../auth/calendar`
   - Click "Save and Continue" through the remaining steps
4. For Application type, select "Desktop application"
5. Give it a name (e.g., "Mikew Performance Tracker")
6. Click "Create"
7. Download the JSON file and rename it to `credentials.json`
8. Place this file in your project root directory

### 4. Configure the Application

1. Open the `.env` file in your project root
2. Update the following values:
   ```
   GOOGLE_CALENDAR_ID=primary
   GOOGLE_CREDENTIALS_FILE=credentials.json
   GOOGLE_TOKEN_FILE=token.json
   ```

### 5. First-Time Authentication

On the first run of the application, you'll need to authenticate with Google:

1. Run the application: `python src/main.py`
2. A browser window will open asking you to sign in to your Google account
3. Select the account you want to use
4. Review the permissions and click "Allow"
5. The application will save a `token.json` file for future use

## Troubleshooting

### "invalid_grant" Error

If you encounter an "invalid_grant" error:
1. Delete the `token.json` file
2. Run the application again to re-authenticate

### Permission Issues

If events aren't being created:
1. Verify that the correct calendar ID is being used
2. Ensure the OAuth consent screen is properly configured
3. Check that the `../auth/calendar` scope is included