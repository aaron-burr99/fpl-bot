# FPL Bot

A Telegram bot that tracks Fantasy Premier League (FPL) scores for the "Second Chance" mini-league.

## Features

- Check the current leaderboard for your FPL mini-league
- Fetches live data from the official FPL API
- Simple button-based interface via Telegram

## Prerequisites

- Python 3.9 or higher
- A Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- FPL Team IDs for each player you want to track

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/fpl-bot.git
   cd fpl-bot
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:

   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```

   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Create a `.env` file** in the project root directory:

   ```bash
   copy .env.example .env
   ```

   Or manually create a `.env` file with the following contents:

   ```env
   API_TOKEN=your_telegram_bot_token_here
   RYAN=12345678
   SEAN_SOO=12345679
   ZHONG_HERN=12345680
   SIYANG=12345681
   ```

2. **Get your Telegram Bot Token:**
   - Open Telegram and search for [@BotFather](https://t.me/botfather)
   - Send `/newbot` and follow the prompts
   - Copy the API token and paste it into your `.env` file

3. **Find FPL Team IDs:**
   - Go to the [FPL website](https://fantasy.premierleague.com/)
   - Navigate to a team's "Points" page
   - The Team ID is in the URL: `https://fantasy.premierleague.com/entry/TEAM_ID/event/1`
   - Add each team ID to the `.env` file with the corresponding variable name

## Running the Bot

Start the bot with:

```bash
python main.py
```

You should see:
```
Bot is starting...
```

The bot will now be running and listening for commands.

## Usage

1. Open Telegram and start a chat with your bot
2. Send `/start` to begin
3. Click "Check 2nd Chance Leaderboard" to see the current standings

## Customization

To track different players, modify the `team_ids` dictionary in `main.py` and add the corresponding environment variables to your `.env` file.

## Troubleshooting

- **Bot not responding:** Ensure your `API_TOKEN` is correct and the bot is running
- **"League 'Second Chance' not found":** The team must be a member of a league named "Second Chance" for the bot to find scores
- **Request failed errors:** Check your internet connection and ensure the FPL API is accessible

## License

MIT License
