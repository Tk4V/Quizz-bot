import logging
import telebot
from quizz import PlayerDataScraper
from config import BOT_TOKEN  # Import BOT_TOKEN from config.py

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Dictionary to store bot status for each chat
bot_enabled_per_chat = {}


# Define the start command handler
@bot.message_handler(commands=['start', 'START'])
def start(message):
    chat_id = message.chat.id
    bot_enabled_per_chat[chat_id] = True
    bot.reply_to(message, "PlayerDataBot started. Send me a player's name to scrape their data.")


# Define the stop command handler
@bot.message_handler(commands=['stop', 'STOP'])
def stop(message):
    chat_id = message.chat.id
    bot_enabled_per_chat[chat_id] = False
    bot.reply_to(message, "PlayerDataBot is now disabled in this chat.")


# Define the help command handler
@bot.message_handler(commands=['help', 'HELP'])
def help(message):
    commands = [
        "/start - Start the bot",
        "/stop - Stop the bot in this chat",
        "/help - Get help with commands"
    ]
    bot.reply_to(message, "Available commands:\n" + "\n".join(commands))


# Define the command handler for scraping player data and unknown commands
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if not bot_enabled_per_chat.get(chat_id, True):
        bot.reply_to(message, "PlayerDataBot is currently disabled in this chat.")
        return

    if message.text.startswith('/'):
        bot.reply_to(message, "Sorry, I don't understand that command. Please use /help to see available commands.")
        return

    player_name = message.text
    player_scraper = PlayerDataScraper(player_name)
    player_scraper.scrape_data()

    try:
        player_scraper.write_to_personal_information()
        player_scraper.write_to_senior_career()
        player_scraper.write_to_international_career()
    except Exception as e:
        bot.reply_to(message, f"An error occurred while processing the data: {str(e)}")
        return

    with open(f"{player_name}.txt", "r") as file:
        data = file.read()
        bot.reply_to(message, f"Player data for {player_name}:\n\n{data}")


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
