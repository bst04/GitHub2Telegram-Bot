import asyncio
import requests
import random
from telegram import Bot
from telegram.error import BadRequest

# Configuration
GITHUB_TOKEN = 'GITHUB_TOKEN'
TELEGRAM_BOT_TOKEN = 'TELEGRAM_BOT_TOKEN'
TELEGRAM_CHANNEL_ID_1 = '-XXXXXXXXXXXXX'  # Replace with your first channel ID
TELEGRAM_CHANNEL_ID_2 = '-XXXXXXXXXXXXX'  # Replace with your second channel ID

# Set to store URLs of sent repositories
sent_repo_urls = set()

# Function to get repositories from GitHub
def get_github_repos(query, page=1):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&page={page}'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error getting repositories from GitHub: {response.status_code} {response.text}")
        return []
    return response.json().get('items', [])

# Asynchronous function to send message to Telegram
async def send_message_to_telegram(bot, message):
    try:
        await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID_1, text=message, parse_mode='Markdown')
        await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID_2, text=message, parse_mode='Markdown')
    except BadRequest as e:
        print(f"Error sending message: {e}")
    except Exception as e:
        print(f"Unexpected exception: {e}")

# Main asynchronous function
async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    query = 'hacking OR cybersecurity'
    sent_messages = 0  # Counter for sent messages
    max_messages = 2  # Maximum number of messages to send per execution

    while True:
        repos = get_github_repos(query)
        valid_repos = [repo for repo in repos if repo.get('stargazers_count', 0) > 50 and repo.get('html_url') not in sent_repo_urls]
        
        if not valid_repos:
            print("No valid repositories found.")
            break
        
        selected_repos = random.sample(valid_repos, min(max_messages, len(valid_repos)))
        
        for repo in selected_repos:
            repo_url = repo.get('html_url')
            repo_stars = repo.get('stargazers_count', 0)
            repo_name = repo.get('name', 'N/A')
            repo_description = repo.get('description', 'N/A')
            
            # Construct the message, customize as you like.
            message = (
                f"*{repo_name}*\n"
                f"{repo_description}\n\n"
                f"🔗 Link: {repo_url}\n"
                f"⭐️ Follow me: https://x.com/__bst04"
            )
            await send_message_to_telegram(bot, message)
            sent_repo_urls.add(repo_url)  # Add URL to the set of sent URLs
            sent_messages += 1
            if sent_messages >= max_messages:
                print("Maximum number of messages sent.")
                return  # Exit the main loop if the limit is reached
        
        await asyncio.sleep(3600)  # Wait 1 hour before searching again

# Run the main function
if __name__ == '__main__':
    asyncio.run(main())
