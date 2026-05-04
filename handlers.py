import telebot
from telebot import types
from data import load_quiz, load_jokes
import random

quiz_data = load_quiz()
jokes = load_jokes()

user_quiz = {}
user_quest = {}

def register(bot: telebot.TeleBot):

    # --- MENU ---
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📚 Викторина", "😂 Анекдот")

        bot.send_message(message.chat.id, "Выбери режим:", reply_markup=markup)

    # --- QUIZ ---
    @bot.message_handler(func=lambda m: m.text == "📚 Викторина")
    def start_quiz(message):
        questions = random.sample(quiz_data, min(10, len(quiz_data)))

        user_quiz[message.chat.id] = {
            "questions": questions,
            "index": 0,
            "score": 0
        }

        send_question(bot, message.chat.id)

    def send_question(bot, chat_id):
        state = user_quiz[chat_id]
        q = state["questions"][state["index"]]

        markup = types.InlineKeyboardMarkup()

        for i, opt in enumerate(q["options"]):
            markup.add(types.InlineKeyboardButton(opt, callback_data=f"quiz_{i}"))

        bot.send_message(chat_id, q["question"], reply_markup=markup)
    # --- QUEST ---
    @bot.message_handler(func=lambda m: m.text == "🧭 Квест")
    def start_quest(message):
        user_quest[message.chat.id] = "start"
        send_node(bot, message.chat.id, "start")

    def send_node(bot, chat_id, node_key):
        node = quest_data[node_key]

        markup = types.InlineKeyboardMarkup()
        for opt in node.get("options", []):
            markup.add(
                types.InlineKeyboardButton(
                    opt["text"],
                    callback_data=f"quest_{opt['next']}"
                )
            )

        bot.send_message(chat_id, node["text"], reply_markup=markup)
    @bot.message_handler(func=lambda m: m.text == "😂 Анекдот")
    def send_joke(message):
        joke = random.choice(jokes)
        bot.send_message(message.chat.id, joke)
    # --- CALLBACK ---
    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        chat_id = call.message.chat.id
        data = call.data

        bot.answer_callback_query(call.id)

        if data.startswith("quiz_"):
            answer = int(data.split("_")[1])
            state = user_quiz.get(chat_id)

            if not state:
                return

            q = state["questions"][state["index"]]
            correct = q["answer"]

            # ✔ правильный ответ
            if answer == correct:
                state["score"] += 1
                bot.send_message(chat_id, "✔ Верно!")

            # ❌ ошибка
            else:
               bot.send_message(
                  chat_id,
                   f"❌ Неверно!\n\n"
                   f"Правильный ответ: {q['options'][correct]}\n\n"
                   f"💡 Объяснение: {q.get('tip', 'Нет объяснения')}"
                )

            state["index"] += 1

            # следующий вопрос
            if state["index"] < len(state["questions"]):
                send_question(bot, chat_id)
            else:
                bot.send_message(
                    chat_id,
                    f"🏁 Квиз завершён!\n"
                    f"Результат: {state['score']}/{len(state['questions'])}"
                )

                user_quiz.pop(chat_id)

        # QUEST
        elif data.startswith("quest_"):
            next_node = data.split("_", 1)[1]
            send_node(bot, chat_id, next_node)