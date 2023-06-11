import pandas as pd
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

df = pd.read_excel("questions.xlsx")

def ask_question(update, context):
    """Задает случайный вопрос из таблицы и отправляет его пользователю."""
    question = df.sample().iloc[0]
    text = question[0] + "\n"
    answers = question[1:].tolist()
    random.shuffle(answers)
    for i, answer in enumerate(answers):
        text += f"{i+1}. {answer}\n"
    context.user_data["correct_answer"] = question[1]
    update.message.reply_text(text)

def check_answer(update, context):
    """Проверяет ответ пользователя и отправляет результат."""
    answer = update.message.text
    correct_answer = context.user_data.get("correct_answer")
    if answer == correct_answer:
        update.message.reply_text("Правильно!")
    else:
        update.message.reply_text(f"Неправильно. Правильный ответ: {correct_answer}")

updater = Updater(token='your_token_here', use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler("start", ask_question)
dispatcher.add_handler(start_handler)

answer_handler = MessageHandler(Filters.text & ~Filters.command, check_answer)
dispatcher.add_handler(answer_handler)

updater.start_polling()


