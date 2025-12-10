from telegram import Update
from telegram.ext import ContextTypes

from connect import DB
from config import ADMINS


async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = DB()
    users = db.get_users()
    d = {}
    for user in users:
        d[db.get_week_exs_count(user)] = user
    user = update.effective_user.id
    text = "<b>Недельный рейтинг:</b><code>\n"
    d_k = sorted(d.keys(), reverse=True)
    for i in range(1, 4):
        text += f"{i}. {db.get_name(d[d_k[i-1]])} - {db.get_week_exs_count(d[d_k[i-1]])}\n"
    text += "</code>\n"
    if db.streak(user):
        st = "🔥"
    else:
        st ="⏳"
    text += (f"<b>Твоя статистика</b>\n" +
            f"Дней в ударном режиме: {db.get_days(user)} {st}\n" +
            f"Cредний результат: {db.get_res(user)}\n" +
            f"Сегодня решено: {db.get_day_exs_count(user)}\n" +
            f"Решено за неделю: {db.get_week_exs_count(user)}\n" +
            f"Всего решено: {db.get_exs_count(user)}\n\n" +
            f"<b>Статистика по заданиям</b><code>\n" +
            f"№   Кол-во  Ср. рез.\n")
    for i in zip(range(1, 13), db.get_exs_c(user), db.get_exs_p(user)):
        text += f"{str(i[0]).ljust(4)}{str(i[1]).ljust(5)}   {(str(i[2]) + ' %').ljust(5)}\n"
    text += f"</code>"

    await update.message.reply_html(text)


async def full_stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = DB()
    if update.effective_user.id not in ADMINS:
        return
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
            f"Сегодня решено: {db.get_day_exs_count(user)}\n" +
            f"Решено за неделю: {db.get_week_exs_count(user)}\n" +
            f"Всего решено: {db.get_exs_count(user)}\n\n" +
            f"<b>Статистика по заданиям</b><code>\n" +
            f"№   Кол-во  Ср. рез.\n")
        for i in zip(range(1, 13), db.get_exs_c(user), db.get_exs_p(user)):
            text += f"{str(i[0]).ljust(4)}{str(i[1]).ljust(5)}   {str(i[2]).ljust(5)}%\n"
        text += f"</code>"

    await update.message.reply_html(text)
