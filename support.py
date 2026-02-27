from telegram import Update
from telegram.ext import ContextTypes
from config import ADMINS


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        msg = " ".join(context.args)
    except KeyError:
        return
    us = f"(@{update.effective_user.username})" if update.effective_user.username else ""
    msg = f"<b>Новое сообщение!</b>\nОт: {update.effective_user.first_name} {us}\n\n" + msg
    for admin in ADMINS:
        await context.bot.send_message(chat_id=admin, text=msg, parse_mode='HTML')
    await update.message.reply_text("Сообщение успешно отправлено!")
