from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters
import telegram

from connect import DB
from config import ADMINS


WAIT_FOR_MESSAGE = 1


async def mailing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #А может отключить проверку - вдруг кто-нибудь полезет в код и найдет дыру, весело будет...
    if update.effective_user.id not in ADMINS:
        return ConversationHandler.END
    await context.bot.send_message(chat_id=update.effective_user.id, text="Пришлите сообщение для рассылки")
    return WAIT_FOR_MESSAGE


async def get_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = DB()
    users = db.get_users()
    commands = {"text": lambda user: context.bot.send_message(chat_id=user, text=update.message.text_html, parse_mode='HTML'),
                "photo": lambda user: context.bot.send_photo(chat_id=user, photo=update.message.photo[-1].file_id, caption=update.message.caption),
                "video": lambda user: context.bot.send_video(chat_id=user, video=update.message.video.file_id, caption=update.message.caption),
                "document": lambda user: context.bot.send_document(chat_id=user, document=update.message.document.file_id, caption=update.message.caption),
                "audio": lambda user: context.bot.send_audio(chat_id=user, audio=update.message.audio.file_id, caption=update.message.caption),
                "voice": lambda user: context.bot.send_voice(chat_id=user, voice=update.message.voice.file_id, caption=update.message.caption),
                "animation": lambda user: context.bot.send_animation(chat_id=user, animation=update.message.animation.file_id, caption=update.message.caption),
                "sticker": lambda user: context.bot.send_sticker(chat_id=user, sticker=update.message.sticker.file_id),
                "video_note": lambda user: context.bot.send_video_note(chat_id=user, video_note=update.message.video_note.file_id),
                }
    if update.message.text:
        cmd = commands["text"]
    elif update.message.photo:
        cmd = commands["photo"]
    elif update.message.video:
        cmd = commands["video"]
    elif update.message.document:
        cmd = commands["document"]
    elif update.message.audio:
        cmd = commands["audio"]
    elif update.message.voice:
        cmd = commands["voice"]
    elif update.message.animation:
        cmd = commands["animation"]
    elif update.message.sticker:
        cmd = commands["sticker"]
    elif update.message.video_note:
        cmd = commands["video_note"]
    else:
        await update.message.reply_text("Неподдерживаемый тип сообщения!")
        return ConversationHandler.END
    for user in users:
        try:
            await cmd(user)
        except telegram.error.BadRequest as e:
            await context.bot.send_message(chat_id=ADMINS[0], text=f"Не удалось отправить пользователю:\n{db.get_username(user)} {db.get_name(user)}\n{str(e)}")
            if str(e) == 'Failed to send message #1 with the error message "user_is_blocked"':
                db.del_user(user)
    await update.message.reply_text("Рассылка совершена!")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Операция прервана!")
    return ConversationHandler.END


mailing_handler = ConversationHandler(
    entry_points=[CommandHandler("mailing", mailing)],
    states={
        WAIT_FOR_MESSAGE: [MessageHandler(filters.ALL & ~filters.COMMAND, get_message)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)
