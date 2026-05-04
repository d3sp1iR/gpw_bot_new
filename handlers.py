import telebot
from telebot import types
from data import load_quiz, load_quest

quest_data = load_quest()
quiz_data = load_quiz()

user_state = {}

def register(bot: telebot.TeleBot):
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Викторина", "Квест", "Прогресс")
        bot.send_message(
            message.chat.id,
            "Добро пожаловать! \nВыбери режим:",
            reply_markup=markup
        )
    
# старт викторины
    @bot.message_handler(func=lambda m: m.text == "📚 Викторина")
    def start_quiz(message):
        user_state[message.chat.id] = {
            "index": 0,
            "score": 0
        }
        send_question(bot, message.chat.id)

    # обработка ответов
    @bot.callback_query_handler(func=lambda call: True)
    def handle_answer(call):
        chat_id = call.message.chat.id
        state = user_state.get(chat_id)

        if not state:
            return

        q_index = state["index"]
        question = quiz_data[q_index]

        chosen = int(call.data)

        if chosen == question["answer"]:
            state["score"] += 1

        state["index"] += 1

        bot.answer_callback_query(call.id)

        if state["index"] < len(quiz_data):
            send_question(bot, chat_id)
        else:
            bot.send_message(
                chat_id,
                f"Квиз завершён!\nРезультат: {state['score']}/{len(quiz_data)}"
            )
            user_state.pop(chat_id, None)


def send_question(bot, chat_id):
    state = user_state[chat_id]
    q = quiz_data[state["index"]]

    markup = types.InlineKeyboardMarkup()

    for i, opt in enumerate(q["options"]):
        markup.add(types.InlineKeyboardButton(opt, callback_data=str(i)))

    bot.send_message(chat_id, q["question"], reply_markup=markup)


def send_node(bot, chat_id, node_key):
    node = quest_data[node_key]

    markup = types.InlineKeyboardMarkup()

    for opt in node.get("options", []):
        markup.add(
            types.InlineKeyboardButton(
                opt["text"],
                callback_data=opt["next"]
            )
        )

    bot.send_message(chat_id, node["text"], reply_markup=markup)

    @bot.message_handler(func=lambda m: m.text == "Квест")
    def start_quest(message):
        user_state[message.chat.id] = "start"
        send_node(bot, message.chat.id, "start")    

    @bot.callback_query_handler(func=lambda call: True)
    def quest_handler(call):
        chat_id = call.message.chat.id
        next_node = call.data

        bot.answer_callback_query(call.id)

        send_node(bot, chat_id, next_node)