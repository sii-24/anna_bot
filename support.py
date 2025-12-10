from telegram import Update
from telegram.ext import ContextTypes
from config import ADMINS


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        msg = " ".join(context.args)
    except KeyError:
        return
    msg = f"<b>Новое сообщение!</b>\n{update.effective_user}\n\n" + msg
    for admin in ADMINS:
        await context.bot.send_message(chat_id=admin, text=msg, parse_mode='HTML')
    await update.message.reply_text("Сообщение успешно отправлено!")
