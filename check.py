from telegram.ext import ContextTypes
from telegram import Update
from connect import DB


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Выполняется check")
    db = DB()
    ans = db.get_answers(update.effective_user.id)
    cor_ans = ans.split(";")
    us_ans = update.message.text.split(";")
    if len(cor_ans) == len(us_ans):
        msg = "Результат: "
        k = 0
        for i in range(len(us_ans)):
            if us_ans[i] == cor_ans[i]:
                k += 1
                msg += f"{i+1} "
            else:
                msg += f"<u>{i+1}</u> "
        res = round(k/len(cor_ans)*100, 1)
        msg += f" - {k}/{len(cor_ans)} баллов ({res}%)"
        msg += f"\nВерные ответы: <tg-spoiler>{ans}</tg-spoiler>"
        t = ["\nТебе есть куда стремиться!", "\nМолодец! Так держать!",]
        msg += t[int(res > 70)]
        db.add_res(update.effective_user.id, res, k)
    else:
        msg = "Некорректные данные! Чтобы пропустить задание поставьте прочерк вместо ответа"
    await update.message.reply_html(msg)