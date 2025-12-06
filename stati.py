from telegram import Update
from telegram.ext import ContextTypes

from connect import DB
from config import ADMINS


async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    db = DB()
    if user in ADMINS:
        text = "<b>Cтатистика</b>"
        users = db.get_users()
        for user in users:
            if db.streak(user):
                st = "🔥"
            else:
                st ="⏳"
            text += (f"\n\n<b>{db.get_name(user)}</b>\n" +
                     f"Дней в ударном режиме: {db.get_days(user)} {st}\n" +
                     f"Cредний результат: {db.get_res(user)}\n" +
                     f"Всего решено заданий: {db.get_exs_count(user)}")
    else:
        if db.streak(user):
            st = "🔥"
        else:
            st ="⏳"
        text = (f"<b>Твоя статистика</b>\n" +
                f"Дней в ударном режиме: {db.get_days(user)} {st}\n" +
                f"Cредний результат: {db.get_res(user)}\n" +
                f"Всего решено заданий: {db.get_exs_count(user)}")
        
    await update.message.reply_html(text)
