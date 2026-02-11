from telegram import InputMediaPhoto, Update
from telegram.ext import ContextTypes
import telegram.constants
import random

from connect import DB
from config import EXAM, ADMINS, EXS_COUNT, BASE_EXS, EXAM_EXS


disc = {
    "math":
    [
        "Задание 1: планиметрия",
        "Задание 2: векторы",
        "Задание 3: стереометрия",
        "Задание 4: простая вероятность",
        "Задание 5: сложная вероятность",
        "Задание 6: простейшие уравнения",
        "Задание 7: вычисления и преобразования",
        "Задание 8: производная",
        "Задание 9: конвертация!",
        "Задание 10: текстовые задачи",
        "Задание 11: графики функций",
        "Задание 12: наибольшее и наименьшее значение функции",
        "Тест! Проверь свои знания",
    ],

    "rus":
    [
        "Задание 1: средства связи предложений в тексте",
        "Задание 2: определение лексического значения слова",
        "Задание 3: стилистический анализ текстов",
        "Задание 4: постановка ударения",
        "Задание 5: употребление паронимов",
        "Задание 6: лексические нормы",
        "Задание 7: морфологические нормы",
        "Задание 8: синтаксические нормы",
        "Задание 9: правописание корней",
        "Задание 10: правописание приставок",
        "Задание 11: правописание суффиксов",
        "Задание 12: правописание личных окончаний глаголов и суффиксов причастий",
        "Задание 13: правописание НЕ и НИ",
        "Задание 14: слитное, дефисное, раздельное написание слов",
        "Задание 15: правописание -Н- и -НН- в суффиксах",
        "Задание 16: пунктуация в сложносочиненном предложении и в предложении с однородными членами",
        "Задание 17: знаки препинания в предложениях с обособленными членами",
        "Задание 18: знаки препинания при словах и конструкциях, не связанных с членами предложения",
        "Задание 19: знаки препинания в сложноподчиненном предложении",
        "Задание 20: знаки препинания в сложных предложениях с разными видами связи",
        "Задание 21: постановка знаков препинания в различных случаях",
        "Задание 22: языковые средства выразительности",
        "Задание 23: смысловая и композиционная целостность текста",
        "Задание 24: функционально-смысловые типы речи",
        "Задание 25: лексическое значение слова",
        "Задание 26: средства связи предложений в тексте",
        "Тест! Проверь свои знания",
    ],

    "inf":
    [

    ],

    "phis":
    [

    ]
}

async def send_manual(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return
    await send(context)


async def send(context: ContextTypes.DEFAULT_TYPE):
    msg = "\n\n<i>Ответы на задания присылай одним сообщением, разделяя их ;\nНапример: 162; 33; 10; 0,2; 0,88; -5; 0,008; 2; 3,5; 8; -4; -8</i>"
    db = DB()
    ex_n = db.get_ex_n()
    test = db.test()
    db.update_ex_n()
    if test:
        msg = disc[EXAM][-1] + msg
        await send_test(context, msg)
    else:
        msg = disc[EXAM][ex_n-1] + msg
        await send_ex(context, msg, ex_n)
    

async def send_ex(context: ContextTypes.DEFAULT_TYPE, msg, ex_n):
    db = DB()
    exs = []
    while len(exs) != EXS_COUNT:
        exs = list(set(random.choices(range(1, BASE_EXS+1), k=EXS_COUNT)))
    media = [InputMediaPhoto(media=open(f"resources/{EXAM}/{ex_n}/ex{exs[0]}.png", "rb"), caption=msg, parse_mode='HTML')]
    cur_var = db.add_exs(exs, ex_n)
    for i in range(1, len(exs)):
        media.append(InputMediaPhoto(media=open(f"resources/{EXAM}/{ex_n}/ex{exs[i]}.png", "rb")))
    users = db.get_users()
    t = await context.bot.send_media_group(chat_id=users[0], media=media)
    db.set_cur_var(users[0], cur_var)
    file_ids = [m.photo[-1].file_id for m in t]
    media = [InputMediaPhoto(media=file_ids[0], caption=msg, parse_mode='HTML')]
    for file_id in file_ids[1:]:
        media.append(InputMediaPhoto(media=file_id))
    for user in users[1:]:
        try:
            await context.bot.send_media_group(chat_id=user, media=media)
            db.set_cur_var(user, cur_var)
        except telegram.error.BadRequest as e:
            await context.bot.send_message(chat_id=ADMINS[0], text=f"Не удалось отправить пользователю:\n{db.get_username(user)} {db.get_name(user)}\n{str(e)}")
            if str(e) == 'Failed to send message #1 with the error message "user_is_blocked"':
                db.del_user(user)


async def send_test(context: ContextTypes.DEFAULT_TYPE, msg):
    exs = list(random.choices(range(1, BASE_EXS+1), k=EXAM_EXS))
    db = DB()
    cur_var = db.add_exs(exs, 0)
    users = db.get_users()
    media = []
    n = 0
    while (EXAM_EXS - n) > 10:
        for i in range(10):
            media.append(InputMediaPhoto(media=open(f"resources/{EXAM}/{n+1}/ex{exs[i]}.png", "rb")))
            n += 1
        t = await context.bot.send_media_group(chat_id=users[0], media=media)
        file_ids = [m.photo[-1].file_id for m in t]
        media = [InputMediaPhoto(media=file_id) for file_id in file_ids]
        for user in users[1:]:
            try:
                await context.bot.send_media_group(chat_id=user, media=media)
            except telegram.error.BadRequest as e:
                await context.bot.send_message(chat_id=ADMINS[0], text=f"Не удалось отправить пользователю:\n{db.get_username(user)} {db.get_name(user)}\n{str(e)}")

    media = [InputMediaPhoto(media=open(f"resources/{EXAM}/{n+1}/ex{exs[n]}.png", "rb"), caption=msg, parse_mode=telegram.constants.ParseMode.HTML)]
    for i in range(1, EXAM_EXS - n):
        media.append(InputMediaPhoto(media=open(f"resources/{EXAM}/{n+i}/ex{exs[n+i]}.png", "rb")))
    t = await context.bot.send_media_group(chat_id=users[0], media=media)
    file_ids = [m.photo[-1].file_id for m in t]
    media = [InputMediaPhoto(media=file_ids[0], caption=msg, parse_mode='HTML')]
    for file_id in file_ids[1:]:
        media.append(InputMediaPhoto(media=file_id))
    for user in users[1:]:
        try:
            await context.bot.send_media_group(chat_id=user, media=media)
            db.set_cur_var(user, cur_var)
        except telegram.error.BadRequest as e:
            await context.bot.send_message(chat_id=ADMINS[0], text=f"Не удалось отправить пользователю:\n{db.get_username(user)} {db.get_name(user)}\n{str(e)}")
            if str(e) == 'Failed to send message #1 with the error message "user_is_blocked"':
                db.del_user(user)


#Доделать!!!
async def rand_var(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = DB()
    user = update.effective_user.id

    if len(context.args) == 0 or (len(context.args) and context.args[0] == 0):
        msg = "Лови свежий вариантик!\n\n<i>Ответы на задания присылай одним сообщением, разделяя их ;\nНапример: 162; 33; 10; 0,2; 0,88; -5; 0,008; 2; 3,5; 8; -4; -8</i>"
        exs = list(random.choices(range(1, EXAM_EXS+1), k=12))
        cur_var = db.add_exs(exs, 0)
        media = []
        for i in range(10):
            media.append(InputMediaPhoto(media=open(f"resources/{EXAM}/{i+1}/ex{exs[i]}.png", "rb")))
        await context.bot.send_media_group(chat_id=user, media=media)
        media = [InputMediaPhoto(media=open(f"resources/img/11/ex{exs[10]}.png", "rb"), caption=msg, parse_mode='HTML')]
        for i in range(11, 12):
            media.append(InputMediaPhoto(media=open(f"resources/img/{i+1}/ex{exs[i]}.png", "rb")))
        db.set_cur_var(user, cur_var)
        await context.bot.send_media_group(chat_id=user, media=media)

    else:
        try:
            ex_n = int(context.args[0])
        except ValueError:
            await update.message.reply_text("Некорректный номер задания")
            return
        if not (1 <= ex_n <= 12):
            await update.message.reply_text("Некорректный номер задания")
            return
        msg = disc[ex_n-1]
        msg += "\n\n<i>Ответы на задания присылай одним сообщением, разделяя их ;\nНапример: 162; 33; 10; 0,2; 0,88; -5; 0,008; 2; 3,5; 8; -4; -8</i>"
        exs = []
        while len(exs) != 10:
            exs = list(set(random.choices(range(1, EXAM_EXS+1), k=10)))
        media = [InputMediaPhoto(media=open(f"resources/img/{ex_n}/ex{exs[0]}.png", "rb"), caption=msg, parse_mode='HTML')]
        cur_var = db.add_exs(exs, ex_n)
        db.set_cur_var(user, cur_var)
        for i in range(1, len(exs)):
            media.append(InputMediaPhoto(media=open(f"resources/img/{ex_n}/ex{exs[i]}.png", "rb")))
        await context.bot.send_media_group(chat_id=user, media=media)
