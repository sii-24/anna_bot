from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import datetime
from zoneinfo import ZoneInfo

from config import TOKEN

from send import send, rand_var, send_manual
from check import check
from noti import noti
from stati import stat, full_stat
from start import start
from reset_streak import reset_streak
from set_name import set_name
from support import support
from mailing import mailing_handler


app = ApplicationBuilder().token(TOKEN).build()


#app.job_queue.run_repeating(
#            send,
#            interval=5
#        )
#
#app.job_queue.run_repeating(
#            reset_streak,
#            interval=10,
#            first=58
#        )


#Отправка задания
app.job_queue.run_daily(
            send,
            time=datetime.time(hour=4, minute=2, tzinfo=ZoneInfo("Europe/Moscow")),
        )

#Сброс ударного режима каждую полночь
app.job_queue.run_daily(
            reset_streak,
            time=datetime.time(hour=4, minute=1, tzinfo=ZoneInfo("Europe/Moscow")),
        )

#Отправка напоминаний
app.job_queue.run_daily(noti, time=datetime.time(hour=6, minute=0, tzinfo=ZoneInfo("Europe/Moscow")), data={"t": 0})
#app.job_queue.run_daily(noti, time=datetime.time(hour=12, minute=0, tzinfo=ZoneInfo("Europe/Moscow")), data={"t": 0})
app.job_queue.run_daily(noti, time=datetime.time(hour=15, minute=0, tzinfo=ZoneInfo("Europe/Moscow")), data={"t": 0})
app.job_queue.run_daily(noti, time=datetime.time(hour=18, minute=0, tzinfo=ZoneInfo("Europe/Moscow")), data={"t": 1})
#app.job_queue.run_daily(noti, time=datetime.time(hour=20, minute=0, tzinfo=ZoneInfo("Europe/Moscow")), data={"t": 1})
app.job_queue.run_daily(noti, time=datetime.time(hour=21, minute=0, tzinfo=ZoneInfo("Europe/Moscow")), data={"t": 1})
#app.job_queue.run_daily(noti, time=datetime.time(hour=22, minute=0, tzinfo=ZoneInfo("Europe/Moscow")), data={"t": 1})
app.job_queue.run_daily(noti, time=datetime.time(hour=23, minute=0, tzinfo=ZoneInfo("Europe/Moscow")), data={"t": 2})
#app.job_queue.run_daily(noti, time=datetime.time(hour=23, minute=15, tzinfo=ZoneInfo("Europe/Moscow")), data={"t": 2})
app.job_queue.run_daily(noti, time=datetime.time(hour=1, minute=0, tzinfo=ZoneInfo("Europe/Moscow")), data={"t": 2})
app.job_queue.run_daily(noti, time=datetime.time(hour=3, minute=0, tzinfo=ZoneInfo("Europe/Moscow")), data={"t": 2})
#app.job_queue.run_daily(noti, time=datetime.time(hour=23, minute=50, tzinfo=ZoneInfo("Europe/Moscow")), data={"t": 2})
#app.job_queue.run_daily(noti, time=datetime.time(hour=23, minute=55, tzinfo=ZoneInfo("Europe/Moscow")), data={"t": 2})


#Запрос случайно сформированного варианта
app.add_handler(CommandHandler("rand_var", rand_var))

#Статистика пользователя
app.add_handler(CommandHandler("stat", stat))
app.add_handler(CommandHandler("full_stat", full_stat))
app.add_handler(CommandHandler("send", send_manual))

#Рассылка
app.add_handler(mailing_handler)

#Установка имени пользователя
app.add_handler(CommandHandler("set_name", set_name))

app.add_handler(CommandHandler("support", support))

app.add_handler(CommandHandler("start", start))

#Сюда попадают все ответы и идут на проверку
app.add_handler(MessageHandler(filters.TEXT, check))

app.run_polling()
