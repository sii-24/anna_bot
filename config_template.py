#заданий в экзамене, заданий в базе
exams = {"math": (12, 100),
         "rus": (26, 100),
         "inf": (),
         "phis": ()
         }

TOKEN = "TOKEN"
ADMINS = []
EXAM = "math" #math, rus, inf, phis
EXAM_EXS = exams[EXAM][0]
BASE_EXS = exams[EXAM][1]
EXS_COUNT = 5 # <= 10

# Изменить:
#  - config
#  - noti + 
#  - send
