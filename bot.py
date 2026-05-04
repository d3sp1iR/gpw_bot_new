import telebot
from config import BOT_TOKEN
print("STEP 1")
import handlers


bot = telebot.TeleBot(BOT_TOKEN)
print("STEP 2")
handlers.register(bot)

print("Bot started...")
bot.infinity_polling()