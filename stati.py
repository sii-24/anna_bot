from telegram import Update
from telegram.ext import ContextTypes

from connect import DB
from config import ADMINS, EXAM_EXS, EXAM, NUMS


async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMINS:
        await full_stat(update, context)
        return
    else:
        db = DB()
        users = db.get_users()
        d = []
        for user in users:
            u = (db.get_name(user), db.get_week_exs_count(user))
            d.append(u)
        d = sorted(d, key=lambda u: u[1], reverse=True)
        text = "<b>Недельный рейтинг:</b><code>\n"
        if len(d) < 5:
            n = len(d)
        else:
            n = 5
        for i in range(n):
            text += f"{i+1}. {d[i][0]} - {d[i][1]}\n"
        text += "</code>\n"
        user = update.effective_user.id
        if db.streak(user):
            st = "🔥"
        else:
            st ="⏳"
        text += (f"<b>Твоя статистика</b>\n" +
                f"Дней в ударном режиме: {db.get_days(user)} {st}\n" +
                f"Дней заморозки: {db.get_freeze(user)} \n" +
                f"Cредний результат: {db.get_res(user)}%\n" +
                f"Сегодня решено: {db.get_day_exs_count(user)}\n" +
                f"Решено за неделю: {db.get_week_exs_count(user)}\n" +
                f"Всего решено: {db.get_exs_count(user)}\n\n" +
                f"<blockquote expandable><b>Статистика по заданиям</b><code>\n" +
                f"№      Кол-во  Ср. рез.\n")
        for i in zip(NUMS[EXAM], db.get_exs_c(user), db.get_exs_p(user)):
            text += f"{str(i[0]).ljust(7)}{str(i[1]).ljust(5)}   {(str(i[2]) + '%').ljust(5)}\n"
        text += f"</code></blockquote>"

        await update.message.reply_html(text)


async def full_stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = DB()
    if update.effective_user.id not in ADMINS:
        return
    text = "<b>Недельный рейтинг</b>"
    users = db.get_users()
    d = []
    for user in users:
        u = [db.get_name(user), db.get_days(user), db.get_freeze(user), db.get_res(user), db.get_day_exs_count(user), 
             db.get_week_exs_count(user), db.get_exs_count(user), db.get_exs_c(user), db.get_exs_p(user), db.get_username(user)]
        if db.streak(user):
            u.append("🔥")
        else:
            u.append("⏳")
        d.append(u)

    l = sorted(d, key=lambda u: u[5], reverse=True)
    text = "<b>Недельный рейтинг:</b><code>\n"
    if len(l) < 5:
        n = len(l)
    else:
        n = 5
    for i in range(n):
        text += f"{i+1}. {l[i][0]} - {l[i][5]}\n"
    text += "</code>"
    for u in sorted(d, key=lambda u: u[6], reverse=True):
        if u[6]:
            text += (f"\n\n<b>{u[0]}</b>\n" +
                f"Дней в ударном режиме: {u[1]} {u[-1]}\n" +
                f"Запас заморозок: {u[2]}\n" +
                f"Cредний результат: {u[3]}%\n" +
                f"Сегодня решено: {u[4]}\n" +
                f"Решено за неделю: {u[5]}\n" +
                f"Всего решено: {u[6]}\n\n" +
                f"<blockquote expandable><b>Статистика по заданиям</b><code>\n" +
                f"№      Кол-во  Ср. рез.\n")
            for i in zip(NUMS, u[7], u[8]):
                text += f"{str(i[0]).ljust(7)}{str(i[1]).ljust(5)}   {str(i[2]).ljust(5)}%\n"
            text += f"</code></blockquote>"

    text += "\n\n<b>Призраки:</b>\n"
    for u in sorted(d, key=lambda u: u[6], reverse=True): 
        if not u[6]:
            us = f"({u[9]})" if u[9] != "None" else ""
            text += f"- {u[0]} {us}\n"

    await update.message.reply_html(text)
