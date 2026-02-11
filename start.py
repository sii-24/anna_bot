from telegram import Update
from telegram.ext import ContextTypes
import sqlite3

from connect import DB
from send import rand_var
from config import ADMINS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = "Привет!\nЭто бот для тренировки тестовых заданий ЕГЭ.\nТеперь ты в ещё одном рабстве! Поздравляю!\n" \
           "Чтобы выжить в этой игре, каждый день решай задания и не забывай присылать мне ответы до 4 утра," \
           " а не то превратишься в тыкву)"
    
    db = DB()
    try:
        db.add_user(update.effective_user)
        print("Пользователь добавлен")
        for admin in ADMINS:
            await context.bot.send_message(chat_id=admin, text="Новый пользователь!\n\n" + str(update.effective_user))
    except sqlite3.IntegrityError:
        print("Пользователь уже существует")

    await update.message.reply_text(text)
    #await rand_var(update, context)
    