#заданий в экзамене, заданий в базе
exams = {"math": (12, 100),
         "rus": (26, 100),
         "inf": (25, 100),
         "phys": (20, 100)
         }

TOKEN = "TOKEN"
ADMINS = []
EXAM = "math" #math, rus, inf, phys
EXAM_EXS = exams[EXAM][0]
BASE_EXS = exams[EXAM][1]
EXS_COUNT = 5 # <= 10

# Изменить:
#  - config
#  - noti
#  - send
#  - stati 
