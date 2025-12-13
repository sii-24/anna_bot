import sqlite3


class DB:

    db_ex = None
    cur_ex = None
    db_us = None
    cur_us = None

    def __init__(self):
        self.db_ex = sqlite3.connect("resources/anna_bot_exs.db")
        self.cur_ex = self.db_ex.cursor()
        self.db_us = sqlite3.connect("anna_bot.db")
        self.cur_us = self.db_us.cursor()
        self.db_ex.execute('CREATE TABLE IF NOT EXISTS exs(id TEXT PRIMARY KEY, answer TEXT) STRICT')
        self.db_us.execute('CREATE TABLE IF NOT EXISTS vars(id INT PRIMARY KEY, answer TEXT, type INT) STRICT')
        self.db_us.execute('CREATE TABLE IF NOT EXISTS users(id INT PRIMARY KEY, username TEXT, name TEXT, \
                            cur_var INT, streak INT, days INT, gen_p TEXT, gen_c INT, week_c INT, day_c INT, \
                            ex_1_c INT, ex_2_c INT, ex_3_c INT, ex_4_c INT, ex_5_c INT, ex_6_c INT, ex_7_c INT, \
                            ex_8_c INT, ex_9_c INT, ex_10_c INT, ex_11_c INT, ex_12_c INT, ex_1_p TEXT, ex_2_p TEXT, \
                            ex_3_p TEXT, ex_4_p TEXT, ex_5_p TEXT, ex_6_p TEXT, ex_7_p TEXT, ex_8_p TEXT, \
                            ex_9_p TEXT, ex_10_p TEXT, ex_11_p TEXT, ex_12_p TEXT) STRICT')
        self.db_us.execute('CREATE TABLE IF NOT EXISTS serv(key TEXT PRIMARY KEY, data INT) STRICT')
        try:
            self.cur_us.execute("INSERT INTO serv VALUES(?, ?)", ("ex_n", 0))
        except:
            ...
        try:
            self.cur_us.execute("INSERT INTO serv VALUES(?, ?)", ("var_id", 1))
        except:
            ...
        self.db_us.commit()
        self.db_ex.commit()


    def __del__(self):
        self.db_us.close()
        self.db_ex.close()

    
    #Работа с базой заданий: автоматическое заполнение ответов 
    def fill_ans(self):
        a = []
        with open("resources/ans.txt") as file:
            for line in file:
                a.append(str(line.split()[-1]))
        k = 0
        for i in range(1, 13):
            for j in range(1, 51):
                self.cur_ex.execute("INSERT INTO exs VALUES(?, ?)", (f"{i}_{j}", a[k]))
                k += 1
        self.db_ex.commit()

    
    #Добавление ответов в базу вариантов
    def add_exs(self, exs, n):
        var_id = int(self.cur_us.execute("SELECT data FROM serv WHERE key == ?", ("var_id", )).fetchone()[0])
        ans = []
        if n == 0:
            for i in range(12):
                ans.append(self.cur_ex.execute("SELECT answer FROM exs WHERE id == ?", (f"{i+1}_{exs[i]}", )).fetchone()[0])
        else:
            for i in exs:
                ans.append(self.cur_ex.execute("SELECT answer FROM exs WHERE id == ?", (f"{n}_{i}", )).fetchone()[0])
        ans = "; ".join(ans)
        self.cur_us.execute("INSERT INTO vars VALUES(?, ?, ?)", (var_id, ans, int(n)))
        self.cur_us.execute("UPDATE serv SET data == ? WHERE key == ?", (var_id + 1, "var_id"))
        self.db_us.commit()
        return var_id


    #Получение номера текущего типа заданий
    def get_ex_n(self):
        res = int(self.cur_us.execute("SELECT data FROM serv WHERE key == ?", ("ex_n", )).fetchone()[0])
        return res
    

    #Обновление текущего номера заданий
    def update_ex_n(self):
        ex_n = int(self.cur_us.execute("SELECT data FROM serv WHERE key == ?", ("ex_n", )).fetchone()[0]) + 1
        if ex_n == 15:
            ex_n = 1
        self.cur_us.execute("UPDATE serv SET data == ? WHERE key == ?", (ex_n, "ex_n"))
        self.db_us.commit()


    #Получение ответов для конкретного пользователя
    def get_answers(self, user):
        cur_var = int(self.cur_us.execute("SELECT cur_var FROM users WHERE id == ?", (user, )).fetchone()[0])
        if cur_var == -1: return None
        res = self.cur_us.execute("SELECT answer FROM vars WHERE id == ?", (cur_var, )).fetchone()[0]
        return res
    
    
    #Добавление пользователя
    def add_user(self, user):
        self.cur_us.execute("INSERT INTO users VALUES( \
                            ?,        ?,             ?,               ?,       ?,      ?,    ?,     ?,     ?,      ?,     ?,      ?,      ?,      ?,      ?,      ?,      ?,      ?,      ?,      ?,       ?,       ?,       ?,      ?,      ?,      ?,      ?,      ?,      ?,      ?,      ?,      ?,       ?,       ?)",
                            (user.id, '@'+user.username, user.first_name, 1,       0,      0,    "100", 0,     0,      0,     0,      0,      0,      0,      0,      0,      0,      0,      0,      0,       0,       0,      "100",   "100",  "100",  "100",  "100",  "100",  "100",  "100",  "100",  "100",   "100",   "100"))
                            #id,      username,      name,            cur_var, streak, days, gen_p, gen_c, week_c, day_c, ex_1_c, ex_2_c, ex_3_c, ex_4_c, ex_5_c, ex_6_c, ex_7_c, ex_8_c, ex_9_c, ex_10_c, ex_11_c, ex_12_c, ex_1_p, ex_2_p, ex_3_p, ex_4_p, ex_5_p, ex_6_p, ex_7_p, ex_8_p, ex_9_p, ex_10_p, ex_11_p, ex_12_p
        self.db_us.commit()


    #Получение списка всех пользователей
    def get_users(self):
        res = [i[0] for i in self.cur_us.execute("SELECT id FROM users").fetchall()]
        return res


    #Получение ника пользователя
    def get_username(self, user):
        res = self.cur_us.execute("SELECT username FROM users WHERE id == ?", (user, )).fetchone()[0]
        return str(res)
    

    #Получение имени пользователя
    def get_name(self, user):
        res = self.cur_us.execute("SELECT name FROM users WHERE id == ?", (user, )).fetchone()[0]
        return str(res)
    

    #Установка имени пользователя
    def set_name(self, user, name):
        self.cur_us.execute("UPDATE users SET name == ? WHERE id == ?", (name, user))
        self.db_us.commit()


    #Установка текущего варианта пользователя
    def set_cur_var(self, user, var):
        self.cur_us.execute("UPDATE users SET cur_var == ? WHERE id == ?", (var, user))
        self.db_us.commit()


    #Сброс ударного режима каждую полночь
    def reset_streak(self):
        users = self.get_users()
        for user in users:
            streak = self.cur_us.execute("SELECT streak FROM users WHERE id == ?", (user, )).fetchone()[0]
            if streak == 0:
                self.cur_us.execute("UPDATE users SET days == ? WHERE id == ?", (0, user))
            self.cur_us.execute("UPDATE users SET streak == ? WHERE id == ?", (0, user))
        self.db_us.commit()
        self.reset_day_exs_count()
        if self.get_ex_n() % 7 == 0:
            self.reset_week_exs_count()


    #Активность ударного режима сегодня
    def streak(self, user):
        res = self.cur_us.execute("SELECT streak FROM users WHERE id == ?", (user, )).fetchone()[0]
        return int(res)
    

    #Получение количества дней в ударном режиме
    def get_days(self, user):
        res = int(self.cur_us.execute("SELECT days FROM users WHERE id == ?", (user, )).fetchone()[0])
        return int(res)
    

    #Получение общего среднего результата
    def get_res(self, user):
        res = self.cur_us.execute("SELECT gen_p FROM users WHERE id == ?", (user, )).fetchone()[0]
        return res
        

    #Получение общего количества решенных заданий
    def get_exs_count(self, user):
        res = self.cur_us.execute("SELECT gen_c FROM users WHERE id == ?", (user, )).fetchone()[0]
        return int(res)
    

    #Получение количества решенных за неделю заданий
    def get_week_exs_count(self, user):
        res = self.cur_us.execute("SELECT week_c FROM users WHERE id == ?", (user, )).fetchone()[0]
        return int(res)
    

    #Получение количества решенных за день заданий
    def get_day_exs_count(self, user):
        res = self.cur_us.execute("SELECT day_c FROM users WHERE id == ?", (user, )).fetchone()[0]
        return int(res)
    

    #Получение процентов по заданиям
    def get_exs_p(self, user):
        res = []
        for i in range(1, 13):
            res.append(self.cur_us.execute(f"SELECT ex_{i}_p FROM users WHERE id == ?", (user, )).fetchone()[0])
        return res


    #Получение количества по заданиям
    def get_exs_c(self, user):
        res = []
        for i in range(1, 13):
            res.append(str(self.cur_us.execute(f"SELECT ex_{i}_c FROM users WHERE id == ?", (user, )).fetchone()[0]))
        return res


    #Сброс недельной статистики
    def reset_week_exs_count(self):
        users = self.get_users()
        for user in users:
            self.cur_us.execute("UPDATE users SET week_c == ? WHERE id == ?", (0, user))
        self.db_us.commit()


    #Сброс дневной статистики
    def reset_day_exs_count(self):
        users = self.get_users()
        for user in users:
            self.cur_us.execute("UPDATE users SET day_c == ? WHERE id == ?", (0, user))
        self.db_us.commit()
 

    #Добавление результатов в базу и ужасно длинная обработка статистики
    def add_res(self, user, res, k, exs_res=None):

        cur_var = int(self.cur_us.execute("SELECT cur_var FROM users WHERE id == ?", (user, )).fetchone()[0])
        ex_n = int(self.cur_us.execute("SELECT type FROM vars WHERE id == ?", (cur_var, )).fetchone()[0])
        self.cur_us.execute("UPDATE users SET cur_var == ? WHERE id == ?", (-1, user))

        #streak + days
        streak = self.cur_us.execute("SELECT streak FROM users WHERE id == ?", (user, )).fetchone()[0]
        if streak == 0:
            self.cur_us.execute("UPDATE users SET streak == ? WHERE id == ?", (1, user))
            days = int(self.cur_us.execute("SELECT days FROM users WHERE id == ?", (user, )).fetchone()[0])
            self.cur_us.execute("UPDATE users SET days == ? WHERE id == ?", (days+1, user))

        #gen_p
        cur_res = float(self.cur_us.execute("SELECT gen_p FROM users WHERE id == ?", (user, )).fetchone()[0])
        n = self.get_days(user)
        if not n: n = 1
        cur_res = (cur_res * n + res) / (self.get_days(user) + 1)
        self.cur_us.execute("UPDATE users SET gen_p == ? WHERE id == ?", (str(round(cur_res, 2)), user))

        #gen_c
        exs_count = int(self.cur_us.execute("SELECT gen_c FROM users WHERE id == ?", (user, )).fetchone()[0])
        self.cur_us.execute("UPDATE users SET gen_c == ? WHERE id == ?", (exs_count+k, user))

        #week_c
        week_c = int(self.cur_us.execute("SELECT week_c FROM users WHERE id == ?", (user, )).fetchone()[0])
        self.cur_us.execute("UPDATE users SET week_c == ? WHERE id == ?", (week_c+k, user))

        #day_c
        day_c = int(self.cur_us.execute("SELECT day_c FROM users WHERE id == ?", (user, )).fetchone()[0])
        self.cur_us.execute("UPDATE users SET day_c == ? WHERE id == ?", (day_c+k, user))

        #ex_p
        if exs_res:
            for i in range(12):
                cur_ex_res = float(self.cur_us.execute(f"SELECT ex_{i+1}_p FROM users WHERE id == ?", (user, )).fetchone()[0])
                n = int(self.cur_us.execute(f"SELECT ex_{i+1}_c FROM users WHERE id == ?", (user, )).fetchone()[0])
                if not n: n = 1
                n = int(self.cur_us.execute(f"SELECT ex_{i+1}_c FROM users WHERE id == ?", (user, )).fetchone()[0])
                if not n: n = 1
                cur_ex_res = (cur_ex_res * n + exs_res[i]) / (n + 1)
                self.cur_us.execute(f"UPDATE users SET ex_{i+1}_p == ? WHERE id == ?", (str(round(cur_ex_res, 2)), user))  

        else:
            cur_ex_res = float(self.cur_us.execute(f"SELECT ex_{ex_n}_p FROM users WHERE id == ?", (user, )).fetchone()[0])
            n = int(self.cur_us.execute(f"SELECT ex_{ex_n}_c FROM users WHERE id == ?", (user, )).fetchone()[0])
            cur_ex_res = (cur_ex_res * n + res) / (n+1)
            self.cur_us.execute(f"UPDATE users SET ex_{ex_n}_p == ? WHERE id == ?", (str(round(cur_ex_res, 2)), user))

        #ex_c
        if exs_res:
            for i in range(12):
                one_ex_count = int(self.cur_us.execute(f"SELECT ex_{i+1}_c FROM users WHERE id == ?", (user, )).fetchone()[0])
                self.cur_us.execute(f"UPDATE users SET ex_{i+1}_c == ? WHERE id == ?", (one_ex_count+exs_res[i], user))
        else:
            one_ex_count = int(self.cur_us.execute(f"SELECT ex_{ex_n}_c FROM users WHERE id == ?", (user, )).fetchone()[0])
            self.cur_us.execute(f"UPDATE users SET ex_{ex_n}_c == ? WHERE id == ?", (one_ex_count+k, user))

        self.db_us.commit()
