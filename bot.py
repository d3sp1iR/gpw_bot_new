import telebot
from config import BOT_TOKEN
import handlers


bot = telebot.TeleBot(BOT_TOKEN)

handlers.register(bot)

print("Bot started...")
bot.infinity_polling()