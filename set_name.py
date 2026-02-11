from telegram import Update
from telegram.ext import ContextTypes

from connect import DB

async def set_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = context.args[0]
    db = DB()
    if all(i not in "<>" for i in name):
        db.set_name(update.effective_user.id, name)
        await update.message.reply_text("Имя успешно изменено!")
    else:
        await update.message.reply_text("Ошибка! Имя не должно содержать символов <>!")
