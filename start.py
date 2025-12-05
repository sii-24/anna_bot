from telegram import Update
from telegram.ext import ContextTypes

from connect import DB
from send import rand_var
from config import ADMIN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = "Привет!\nЭто бот для тренировки теста из профмата.\nТеперь ты в ещё одном рабстве! Поздравляю!\n" \
           "Чтобы выжить в этой игре, каждый день решай задания и не забывай присылать мне ответы до полуночи," \
           " а не то превратишься в тыкву)"
    
    db = DB()
    try:
        db.add_user(update.effective_user.id)
        print("Пользователь добавлен")
        context.bot.send_message(chat_id=ADMIN, text="Новый пользователь!\n\n" + str(update.effective_user))
    except:
        print("Пользователь уже существует")

    await update.message.reply_text(text)
    await rand_var(update, context)
    