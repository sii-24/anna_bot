from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import datetime
from zoneinfo import ZoneInfo

from config import TOKEN

from send import send, rand_var
from check import check
from noti import noti
from start import start
from reset_streak import reset_streak


app = ApplicationBuilder().token(TOKEN).build()


#app.job_queue.run_repeating(
#            send,
#            interval=30
#        )


#Отправка задания
app.job_queue.run_daily(
            send,
            time=datetime.time(hour=0, minute=2, tzinfo=ZoneInfo("Europe/Moscow")),
        )

#Сброс ударного режима каждую полночь
app.job_queue.run_daily(
            reset_streak,
            time=datetime.time(hour=0, minute=1, tzinfo=ZoneInfo("Europe/Moscow")),
        )

#Отправка напоминаний
app.job_queue.run_daily(noti, time=datetime.time(hour=6, minute=0, tzinfo=ZoneInfo("Europe/Moscow")))
app.job_queue.run_daily(noti, time=datetime.time(hour=12, minute=0, tzinfo=ZoneInfo("Europe/Moscow")))
app.job_queue.run_daily(noti, time=datetime.time(hour=15, minute=0, tzinfo=ZoneInfo("Europe/Moscow")))
app.job_queue.run_daily(noti, time=datetime.time(hour=18, minute=0, tzinfo=ZoneInfo("Europe/Moscow")))
app.job_queue.run_daily(noti, time=datetime.time(hour=20, minute=0, tzinfo=ZoneInfo("Europe/Moscow")))
app.job_queue.run_daily(noti, time=datetime.time(hour=21, minute=0, tzinfo=ZoneInfo("Europe/Moscow")))
app.job_queue.run_daily(noti, time=datetime.time(hour=22, minute=0, tzinfo=ZoneInfo("Europe/Moscow")))
app.job_queue.run_daily(noti, time=datetime.time(hour=23, minute=0, tzinfo=ZoneInfo("Europe/Moscow")))
app.job_queue.run_daily(noti, time=datetime.time(hour=23, minute=15, tzinfo=ZoneInfo("Europe/Moscow")))
app.job_queue.run_daily(noti, time=datetime.time(hour=23, minute=30, tzinfo=ZoneInfo("Europe/Moscow")))
app.job_queue.run_daily(noti, time=datetime.time(hour=23, minute=45, tzinfo=ZoneInfo("Europe/Moscow")))
app.job_queue.run_daily(noti, time=datetime.time(hour=23, minute=50, tzinfo=ZoneInfo("Europe/Moscow")))
app.job_queue.run_daily(noti, time=datetime.time(hour=23, minute=55, tzinfo=ZoneInfo("Europe/Moscow")))


#Запрос случайно сформированного варианта
app.add_handler(CommandHandler("rand_var", rand_var))

app.add_handler(CommandHandler("start", start))

#Сюда попадают все ответы и идут на проверку
app.add_handler(MessageHandler(filters.ALL, check))

app.run_polling()
