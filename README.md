# GitHub2Telegram-Bot

A Python script to fetch popular GitHub repositories and send their details to Telegram channels. Make sure to give the repo a ⭐️! 

**Check my other links:** https://privacidad.me/@bst04


## Features

- Filters by **⭐️** **count** and **🚫** **DUPLICATES**.
- Sends details (name, description, link) to Telegram channels.

## Requirements

- [x] Python 3.7+ 
- [x] GitHub personal access token
- [x] Telegram bot token
- [x] Telegram channel IDs

## Setup

1. Install dependencies:
    ```bash
    pip install requests python-telegram-bot
    ```
2. Update the script with your credentials:
    - `GITHUB_TOKEN`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHANNEL_ID_1`, `TELEGRAM_CHANNEL_ID_2`.

## Usage

Run the script:
```bash
python git2telegram_bot.py
```

## Notes

- Ensure proper permissions for GitHub and Telegram.
- Use responsibly under respective terms of service.
