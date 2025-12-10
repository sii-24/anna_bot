from telegram.ext import ContextTypes
from telegram import Update

from connect import DB
from stati import stat


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = DB()
    user = update.effective_user.id
    ans = db.get_answers(user)
    us_ans = update.message.text.strip(" ;,.").split(";")
    if ans and len(ans.split(";")) == len(us_ans):
        cor_ans = ans.split(";")
        exs_res = []
        msg = "Результат: "
        k = 0
        for i in range(len(us_ans)):
            if us_ans[i] == cor_ans[i]:
                k += 1
                msg += f"{i+1} "
                exs_res.append(1)
            else:
                msg += f"<u>{i+1}</u> "
                exs_res.append(0)
        res = k/len(cor_ans)*100

        if len(cor_ans) == 12:
            db.add_res(user, res, k, exs_res)
        elif len(cor_ans) == 10:
            db.add_res(user, res, k)
            
        msg += f" - {k}/{len(cor_ans)} ({round(res, 2)}%)"
        msg += f"\nВерные ответы: <tg-spoiler>{ans}</tg-spoiler>"
        t = ["\nТебе есть куда стремиться!", "\nМолодец! Так держать!",]
        msg += t[int(res > 70)]
        msg += (f"\n\nУдарный режим: {db.get_days(user)} 🔥\n" +
               f"Средний балл: {db.get_res(user)}\n" +
               f"Сегодня решено: {db.get_day_exs_count(user)}\n" +
               f"Решено за неделю: {db.get_week_exs_count(user)}\n" +
               f"Всего решено: {db.get_exs_count(user)}")
        await update.message.reply_html(msg)
        if db.get_ex_n() % 7 == 0:
            await stat(update, context)

    else:
        msg = "Некорректные данные! Чтобы пропустить задание поставьте прочерк вместо ответа"
        await update.message.reply_html(msg)
