import os
from telebot import TeleBot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = TeleBot(BOT_TOKEN)

bot.remove_webhook()