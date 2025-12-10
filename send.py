from telegram import InputMediaPhoto, Update
from telegram.ext import ContextTypes
import telegram.constants
import random

from connect import DB
from config import EX


disc = [
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
        ]


async def send(context: ContextTypes.DEFAULT_TYPE):
    db = DB()
    db.update_ex_n()
    ex_n = db.get_ex_n()
    msg = "\n\n<i>Ответы на задания присылай одним сообщением, разделяя их ;\nНапример: 162; 33; 10; 0,2; 0,88; -5; 0,008; 2; 3,5; 8; -4; -8</i>"
    if ex_n % 7 == 0:
        msg = disc[-1] + msg
        await send_test(context, msg)
    else:
        if ex_n > 7:
            ex_n -= 1
        msg = disc[ex_n-1] + msg
        await send_ex(context, msg, ex_n)
    

async def send_ex(context: ContextTypes.DEFAULT_TYPE, msg, ex_n):
    db = DB()
    exs = []
    while len(exs) != 10:
        exs = list(set(random.choices(range(1, EX+1), k=10)))
    media = [InputMediaPhoto(media=open(f"resources/img/{ex_n}/ex{exs[0]}.png", "rb"), caption=msg, parse_mode='HTML')]
    cur_var = db.add_exs(exs, ex_n)
    for i in range(1, len(exs)):
        media.append(InputMediaPhoto(media=open(f"resources/img/{ex_n}/ex{exs[i]}.png", "rb")))
    users = db.get_users()
    t = await context.bot.send_media_group(chat_id=users[0], media=media)
    db.set_cur_var(users[0], cur_var)
    file_ids = [m.photo[-1].file_id for m in t]
    media = [InputMediaPhoto(media=file_ids[0], caption=msg, parse_mode='HTML')]
    for file_id in file_ids[1:]:
        media.append(InputMediaPhoto(media=file_id))
    for user in users[1:]:
        db.set_cur_var(user, cur_var)
        await context.bot.send_media_group(chat_id=user, media=media)


async def send_test(context: ContextTypes.DEFAULT_TYPE, msg):
    exs = list(random.choices(range(1, EX+1), k=12))
    db = DB()
    cur_var = db.add_exs(exs, 0)
    users = db.get_users()
    media = []
    for i in range(10):
        media.append(InputMediaPhoto(media=open(f"resources/img/{i+1}/ex{exs[i]}.png", "rb")))
    t = await context.bot.send_media_group(chat_id=users[0], media=media)
    file_ids = [m.photo[-1].file_id for m in t]
    media = [InputMediaPhoto(media=file_id) for file_id in file_ids]
    for user in users[1:]:
        await context.bot.send_media_group(chat_id=user, media=media)
    media = [InputMediaPhoto(media=open(f"resources/img/11/ex{exs[10]}.png", "rb"), caption=msg, parse_mode=telegram.constants.ParseMode.HTML)]
    for i in range(11, 12):
        media.append(InputMediaPhoto(media=open(f"resources/img/{i+1}/ex{exs[i]}.png", "rb")))
    t = await context.bot.send_media_group(chat_id=users[0], media=media)
    db.set_cur_var(users[0], cur_var)
    file_ids = [m.photo[-1].file_id for m in t]
    media = [InputMediaPhoto(media=file_ids[0], caption=msg, parse_mode='HTML')]
    for file_id in file_ids[1:]:
        media.append(InputMediaPhoto(media=file_id))
    for user in users[1:]:
        db.set_cur_var(user, cur_var)
        await context.bot.send_media_group(chat_id=user, media=media)


async def rand_var(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = DB()
    user = update.effective_user.id

    if len(context.args) == 0 or (len(context.args) and context.args[0] == 0):
        msg = "Лови свежий вариантик!\n\n<i>Ответы на задания присылай одним сообщением, разделяя их ;\nНапример: 162; 33; 10; 0,2; 0,88; -5; 0,008; 2; 3,5; 8; -4; -8</i>"
        exs = list(random.choices(range(1, EX+1), k=12))
        cur_var = db.add_exs(exs, 0)
        media = []
        for i in range(10):
            media.append(InputMediaPhoto(media=open(f"resources/img/{i+1}/ex{exs[i]}.png", "rb")))
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
            exs = list(set(random.choices(range(1, EX+1), k=10)))
        media = [InputMediaPhoto(media=open(f"resources/img/{ex_n}/ex{exs[0]}.png", "rb"), caption=msg, parse_mode='HTML')]
        cur_var = db.add_exs(exs, ex_n)
        db.set_cur_var(user, cur_var)
        for i in range(1, len(exs)):
            media.append(InputMediaPhoto(media=open(f"resources/img/{ex_n}/ex{exs[i]}.png", "rb")))
        await context.bot.send_media_group(chat_id=user, media=media)
