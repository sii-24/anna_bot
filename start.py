from telegram import Update
from telegram.ext import ContextTypes
import sqlite3

from connect import DB
from send import rand_var
from config import ADMINS

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ('Привет!\n' +
            'Это бот для тренировки тестовых заданий ЕГЭ.\n' +
            'Теперь ты в ещё одном рабстве! Поздравляю!\n' +
            'Чтобы выжить в этой игре, каждый день решай задания и не забывай присылать мне ответы до 4 утра, а не то превратишься в тыкву)\n\n' +
            '<b>Доступные команды:</b>\n' +
            '/help - справка\n' +
            '/stat - посмотреть свою статистику\n' +
            '/support - задать вопрос, например вот так <code>"/support А как пройти в библиотеку?"</code>\n' +
            '/set_name - установить имя, которое будет отображаться в рейтинге, например <code>"/set_name Si!"</code>\n')
    
    await update.message.reply_html(text)
    

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = DB()
    try:
        db.add_user(update.effective_user)
        print("Пользователь добавлен")
        for admin in ADMINS:
            await context.bot.send_message(chat_id=admin, text="Новый пользователь!\n\n" + str(update.effective_user))
    except sqlite3.IntegrityError:
        print("Пользователь уже существует")

    await help(update, context)
    #await rand_var(update, context)
    