import telebot
import handlers 

bot = telebot.TeleBot("8758647298:AAHGX_LckOWqY4pru08BsqEbwZGSaay6kyQ")

handlers.register(bot)

print("Работает вроде")
bot.infinity_polling()