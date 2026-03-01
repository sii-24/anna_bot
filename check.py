from telegram.ext import ContextTypes
from telegram import Update

from connect import DB
from config import EXAM_EXS, EXS_COUNT, NUMS


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = DB()
    user = update.effective_user.id
    ans = db.get_answers(user)
    if not ans:
        msg = "Вы уже отвечали на это задание!"
        await update.message.reply_html(msg)
        return
    us_ans = [i.strip().lower() for i in update.message.text.strip(" ;,.").replace(':', ';').split(';')]
    if len(ans.split(";")) == len(us_ans):
        cor_ans = [i.strip() for i in ans.split(';')]
        exs_res = []
        msg = "Результат: "
        k = 0
        for i in range(len(us_ans)):
            ca = [a.strip() for a in cor_ans[i].split('|')]
            if us_ans[i] in ca or us_ans[i].replace(' ', '') in ca:
                k += 1
                msg += f"{NUMS[i]} "
                exs_res.append(100)
            else:
                msg += f"<u>{NUMS[i]}</u> "
                exs_res.append(0)
        res = k/len(cor_ans)*100

        if len(cor_ans) == EXAM_EXS:
            db.add_res(user, res, k, exs_res)
        elif len(cor_ans) == EXS_COUNT:
            db.add_res(user, res, k)
            
        msg += f"- {k}/{len(cor_ans)} ({round(res, 2)}%)\n"
        t = ["Тебе есть куда стремиться!", "Молодец! Так держать!"]
        msg += t[int(res > 70)]

        msg += "\n\nВерные ответы: <tg-spoiler>\n"
        for i in range(len(cor_ans)):
            msg += f"{NUMS[i]}. {cor_ans[i]}\n"
        msg += "</tg-spoiler>"

        msg += (f"\nУдарный режим: {db.get_days(user)} 🔥\n" +
               f"Запас заморозок: {db.get_freeze(user)}\n" +
               f"Средний балл: {db.get_res(user)}\n" +
               f"Сегодня решено: {db.get_day_exs_count(user)}\n" +
               f"Решено за неделю: {db.get_week_exs_count(user)}\n" +
               f"Всего решено: {db.get_exs_count(user)}")
        await update.message.reply_html(msg)

    else:
        msg = "Некорректные данные! Чтобы пропустить задание поставьте прочерк вместо ответа"
        await update.message.reply_html(msg)
