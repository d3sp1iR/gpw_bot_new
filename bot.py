import telebot
import handlers 

BOT_TOKEN = "8758647298:AAHGX_LckOWqY4pru08BsqEbwZGSaay6kyQ"
bot = telebot.TeleBot(BOT_TOKEN)

handlers.register(bot)

print("Работает вроде")
bot.infinity_polling()