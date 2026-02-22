import sqlite3

from config import EXAM, EXAM_EXS, exams


class DB:

    db_ex = None
    cur_ex = None
    db_us = None
    cur_us = None

    def __init__(self):
        self.db_us = sqlite3.connect("anna_bot.db")
        self.cur_us = self.db_us.cursor()
        self.db_us.execute(f'CREATE TABLE IF NOT EXISTS vars (id INT PRIMARY KEY, answer TEXT, type INT) STRICT')
        self.db_us.execute('CREATE TABLE IF NOT EXISTS users(id INT PRIMARY KEY, username TEXT, name TEXT, \
                            cur_var INT, streak INT, freeze INT, days INT, gen_p TEXT, gen_c INT, week_c INT, \
                            day_c INT, exs_p TEXT, exs_c TEXT) STRICT')
        self.db_us.execute('CREATE TABLE IF NOT EXISTS serv(key TEXT PRIMARY KEY, data INT) STRICT')
        try:
            self.cur_us.execute("INSERT INTO serv VALUES(?, ?)", ("ex_n", 1))
        except:
            ...
        try:
            self.cur_us.execute("INSERT INTO serv VALUES(?, ?)", ("var_id", 1))
        except:
            ...
        try:
            self.cur_us.execute("INSERT INTO serv VALUES(?, ?)", ("test", 0))
        except:
            ...
        self.db_us.commit()


    def __del__(self):
        self.db_us.close()

    
    #Работа с базой заданий: автоматическое заполнение ответов 
    def fill_ans(self, exam):
        exam_exs = exams[exam][0]
        base_exs = exams[exam][1]
        self.db_ex = sqlite3.connect("resources/anna_bot_exs.db")
        self.db_ex.execute(f'CREATE TABLE IF NOT EXISTS {exam} (id TEXT PRIMARY KEY, answer TEXT) STRICT')
        self.cur_ex = self.db_ex.cursor()
        a = []
        with open(f"resources/{exam}/ans.txt") as file:
            for line in file:
                a.append(' '.join(line.split()[2:]))
        k = 0
        for i in range(1, exam_exs+1):
            for j in range(1, base_exs+1):
                self.cur_ex.execute(f"INSERT INTO {exam} VALUES(?, ?)", (f"{i}_{j}", a[k]))
                k += 1
        self.db_ex.commit()
        self.db_ex.close()

    
    #Добавление ответов в базу вариантов
    def add_exs(self, exs, n):
        self.db_ex = sqlite3.connect("resources/anna_bot_exs.db")
        self.cur_ex = self.db_ex.cursor()
        var_id = int(self.cur_us.execute("SELECT data FROM serv WHERE key = ?", ("var_id", )).fetchone()[0])
        ans = []
        if n == 0:
            for i in range(EXAM_EXS):
                ans.append(self.cur_ex.execute(f"SELECT answer FROM {EXAM} WHERE id = ?", (f"{i+1}_{exs[i]}", )).fetchone()[0])
        else:
            for i in exs:
                ans.append(self.cur_ex.execute(f"SELECT answer FROM {EXAM} WHERE id = ?", (f"{n}_{i}", )).fetchone()[0])
        ans = "; ".join(ans)
        self.cur_us.execute("INSERT INTO vars VALUES(?, ?, ?)", (var_id, ans, int(n)))
        self.cur_us.execute("UPDATE serv SET data = ? WHERE key = ?", (var_id+1, "var_id"))
        self.db_us.commit()
        self.db_ex.commit()
        self.db_ex.close()
        return var_id


    #Получение номера текущего типа заданий
    def get_ex_n(self):
        res = int(self.cur_us.execute("SELECT data FROM serv WHERE key = ?", ("ex_n", )).fetchone()[0])
        return res
    
    def test(self):
        return not bool(self.cur_us.execute("SELECT data FROM serv WHERE key = ?", ("test", )).fetchone()[0])
    

    #Обновление текущего номера заданий
    def update_ex_n(self):
        ex_n = int(self.cur_us.execute("SELECT data FROM serv WHERE key = ?", ("ex_n", )).fetchone()[0])
        test = int(self.cur_us.execute("SELECT data FROM serv WHERE key = ?", ("test", )).fetchone()[0])
        if test:
            ex_n += 1
            if ex_n > EXAM_EXS:
                ex_n = 1
        test += 1
        if test == 7:
            test = 0
        self.cur_us.execute("UPDATE serv SET DATA = ? WHERE key = ?", (test, "test"))    
        self.cur_us.execute("UPDATE serv SET data = ? WHERE key = ?", (ex_n, "ex_n"))
        self.db_us.commit()


    #Получение ответов для конкретного пользователя
    def get_answers(self, user):
        cur_var = int(self.cur_us.execute("SELECT cur_var FROM users WHERE id = ?", (user, )).fetchone()[0])
        if cur_var == -1: return None
        res = self.cur_us.execute("SELECT answer FROM vars WHERE id = ?", (cur_var, )).fetchone()[0]
        return res
    
    
    #Добавление пользователя
    def add_user(self, user):
        us = user.username
        if us:
            us = '@' + us
        self.cur_us.execute("INSERT INTO users VALUES( \
                            ?,        ?,        ?,               ?,       ?,      ?,      ?,    ?,     ?,     ?,      ?,      ?,                ?)", 
                            (user.id, us,       user.first_name, 1,       1,      1,      0,    "100", 0,     0,      0,      "100 "*EXAM_EXS,  "0 "*EXAM_EXS)) 
                            #id,      username, name,            cur_var, streak, freeze, days, gen_p, gen_c, week_c, day_c,  exs_p,            exs_c
        self.db_us.commit()

    def del_user(self, user):
        self.cur_us.execute("DELETE FROM users WHERE id = ?", (user, )).fetchone()[0]
        self.db_us.commit()

    #Получение списка всех пользователей
    def get_users(self):
        res = [i[0] for i in self.cur_us.execute("SELECT id FROM users").fetchall()]
        return res


    #Получение ника пользователя
    def get_username(self, user):
        res = self.cur_us.execute("SELECT username FROM users WHERE id = ?", (user, )).fetchone()[0]
        return str(res)
    

    #Получение имени пользователя
    def get_name(self, user):
        res = self.cur_us.execute("SELECT name FROM users WHERE id = ?", (user, )).fetchone()[0]
        return str(res)
    

    #Установка имени пользователя
    def set_name(self, user, name):
        self.cur_us.execute("UPDATE users SET name = ? WHERE id = ?", (name, user))
        self.db_us.commit()


    #Установка текущего варианта пользователя
    def set_cur_var(self, user, var):
        self.cur_us.execute("UPDATE users SET cur_var = ? WHERE id = ?", (var, user))
        self.db_us.commit()


    #Сброс ударного режима каждую полночь
    def reset_streak(self):
        users = self.get_users()
        for user in users:
            streak = self.cur_us.execute("SELECT streak FROM users WHERE id = ?", (user, )).fetchone()[0]
            freeze = self.cur_us.execute("SELECT freeze FROM users WHERE id = ?", (user, )).fetchone()[0]
            if streak == 0:
                if freeze == 0:
                    self.cur_us.execute("UPDATE users SET days == ? WHERE id = ?", (0, user))
                else:
                    self.cur_us.execute("UPDATE users SET freeze == ? WHERE id = ?", (freeze-1, user))
            self.cur_us.execute("UPDATE users SET streak == ? WHERE id = ?", (0, user))
        self.db_us.commit()
        self.reset_day_exs_count()
        if self.get_ex_n() % 7 == 0:
            self.reset_week_exs_count()


    #Активность ударного режима сегодня
    def streak(self, user):
        res = self.cur_us.execute("SELECT streak FROM users WHERE id = ?", (user, )).fetchone()[0]
        return int(res)
    
    #Количество дней заморозки
    def get_freeze(self, user):
        res = self.cur_us.execute("SELECT freeze FROM users WHERE id = ?", (user, )).fetchone()[0]
        return int(res)

    #Получение количества дней в ударном режиме
    def get_days(self, user):
        res = int(self.cur_us.execute("SELECT days FROM users WHERE id = ?", (user, )).fetchone()[0])
        return int(res)
    

    #Получение общего среднего результата
    def get_res(self, user):
        res = self.cur_us.execute("SELECT gen_p FROM users WHERE id = ?", (user, )).fetchone()[0]
        return res
        

    #Получение общего количества решенных заданий
    def get_exs_count(self, user):
        res = self.cur_us.execute("SELECT gen_c FROM users WHERE id = ?", (user, )).fetchone()[0]
        return int(res)
    

    #Получение количества решенных за неделю заданий
    def get_week_exs_count(self, user):
        res = self.cur_us.execute("SELECT week_c FROM users WHERE id = ?", (user, )).fetchone()[0]
        return int(res)
    

    #Получение количества решенных за день заданий
    def get_day_exs_count(self, user):
        res = self.cur_us.execute("SELECT day_c FROM users WHERE id = ?", (user, )).fetchone()[0]
        return int(res)
    

    #Получение процентов по заданиям
    def get_exs_p(self, user):
        res = [float(i) for i in self.cur_us.execute("SELECT exs_p FROM users WHERE id = ?", (user, )).fetchone()[0].split()]
        return res


    #Получение количества по заданиям
    def get_exs_c(self, user):
        res = [int(i) for i in self.cur_us.execute("SELECT exs_c FROM users WHERE id = ?", (user, )).fetchone()[0].split()]
        return res


    #Сброс недельной статистики
    def reset_week_exs_count(self):
        users = self.get_users()
        for user in users:
            self.cur_us.execute("UPDATE users SET week_c = ? WHERE id = ?", (0, user))
        self.db_us.commit()


    #Сброс дневной статистики
    def reset_day_exs_count(self):
        users = self.get_users()
        for user in users:
            self.cur_us.execute("UPDATE users SET day_c = ? WHERE id = ?", (0, user))
        self.db_us.commit()
 

    #Добавление результатов в базу и ужасно длинная обработка статистики
    def add_res(self, user, res, k, exs_res=None):
        n = self.get_days(user)
        if not n: n = 1

        cur_var = int(self.cur_us.execute("SELECT cur_var FROM users WHERE id = ?", (user, )).fetchone()[0])
        ex_n = int(self.cur_us.execute("SELECT type FROM vars WHERE id = ?", (cur_var, )).fetchone()[0]) - 1
        self.cur_us.execute("UPDATE users SET cur_var == ? WHERE id = ?", (-1, user))

        #streak + days
        streak = self.cur_us.execute("SELECT streak FROM users WHERE id = ?", (user, )).fetchone()[0]
        freeze = self.cur_us.execute("SELECT freeze FROM users WHERE id = ?", (user, )).fetchone()[0]
        if streak == 0:
            self.cur_us.execute("UPDATE users SET streak = 1 WHERE id = ?", (user, ))
            days = int(self.cur_us.execute("SELECT days FROM users WHERE id = ?", (user, )).fetchone()[0])
            self.cur_us.execute("UPDATE users SET days = ? WHERE id = ?", (days+1, user))
            if (days + 1) % 14 == 0:
                self.cur_us.execute("UPDATE users SET freeze = ? WHERE id = ?", (freeze+1, user))

        #gen_c
        exs_count = int(self.cur_us.execute("SELECT gen_c FROM users WHERE id = ?", (user, )).fetchone()[0])
        self.cur_us.execute("UPDATE users SET gen_c = ? WHERE id = ?", (exs_count+k, user))

        #gen_p
        cur_res = float(self.cur_us.execute("SELECT gen_p FROM users WHERE id = ?", (user, )).fetchone()[0])
        cur_res = (cur_res * exs_count + res) / (exs_count + 1)
        self.cur_us.execute("UPDATE users SET gen_p = ? WHERE id = ?", (str(round(cur_res, 2)), user))

        #week_c
        week_c = int(self.cur_us.execute("SELECT week_c FROM users WHERE id = ?", (user, )).fetchone()[0])
        self.cur_us.execute("UPDATE users SET week_c = ? WHERE id = ?", (week_c+k, user))

        #day_c
        day_c = int(self.cur_us.execute("SELECT day_c FROM users WHERE id = ?", (user, )).fetchone()[0])
        self.cur_us.execute("UPDATE users SET day_c = ? WHERE id = ?", (day_c+k, user))

        #exs_p and exs_c
        exs_p = [float(i) for i in self.cur_us.execute("SELECT exs_p FROM users WHERE id = ?", (user, )).fetchone()[0].split()]
        exs_c = [int(i) for i in self.cur_us.execute("SELECT exs_c FROM users WHERE id = ?", (user, )).fetchone()[0].split()] 
        if exs_res:
            for i in range(len(exs_c)):
                exs = exs_c[i] if exs_c[i] > 0 else 1
                exs_p[i] = (exs_p[i] * exs + exs_res[i]) / (exs + 1)
                if exs_res[i]:
                    exs_c[i] += 1
        else:
            exs = exs_c[ex_n] if exs_c[ex_n] > 0 else 1
            exs_p[ex_n] = (exs_p[ex_n] * exs + res*k) / (exs+k)
            exs_c[ex_n] += k
        self.cur_us.execute(f"UPDATE users SET exs_p = ? WHERE id = ?", (' '.join([str(round(i, 2)) for i in exs_p]), user)) 
        self.cur_us.execute(f"UPDATE users SET exs_c = ? WHERE id = ?", (' '.join([str(i) for i in exs_c]), user)) 

        self.db_us.commit()
