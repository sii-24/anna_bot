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
        self.db_ex.execute('CREATE TABLE IF NOT EXISTS exs(id PRIMARY KEY, answer TEXT)')
        self.db_us.execute('CREATE TABLE IF NOT EXISTS vars(id PRIMARY KEY, answer)')
        self.db_us.execute('CREATE TABLE IF NOT EXISTS users(id PRIMARY KEY, streak INT, days INT, res REAL, exs_count INT, cur_var TEXT)')
        self.db_us.execute('CREATE TABLE IF NOT EXISTS serv(key PRIMARY KEY, data)')
        try:
            self.cur_us.execute("INSERT INTO serv VALUES(?, ?)", ("ex_n", 1))
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


    def streak(self, user):
        res = self.cur_us.execute("SELECT streak FROM users WHERE id == ?", (user, )).fetchone()
        return bool(res)
    

    def get_ex_n(self):
        res = int(self.cur_us.execute("SELECT data FROM serv WHERE key == ?", ("ex_n", )).fetchone()[0])
        return res
    

    def update_ex_n(self):
        ex_n = int(self.cur_us.execute("SELECT data FROM serv WHERE key == ?", ("ex_n", )).fetchone()[0]) + 1
        if ex_n == 15:
            ex_n = 1
        self.cur_us.execute("UPDATE serv SET data == ? WHERE key == ?", (ex_n, "ex_n"))
        self.db_us.commit()
 

    def add_res(self, user, res, k):
        cur_res = self.cur_us.execute("SELECT res FROM users WHERE id == ?", (user, )).fetchone()[0]
        cur_res = (cur_res + res) / 2
        self.cur_us.execute("UPDATE users SET res == ? WHERE id == ?", (cur_res, user))
        streak = self.cur_us.execute("SELECT streak FROM users WHERE id == ?", (user, )).fetchone()[0]
        if streak == 0:
            self.cur_us.execute("UPDATE users SET streak == ? WHERE id == ?", (1, user))
            days = self.cur_us.execute("SELECT days FROM users WHERE id == ?", (user, )).fetchone()[0]
            self.cur_us.execute("UPDATE users SET days == ? WHERE id == ?", (days+1, user))
        exs_count = self.cur_us.execute("SELECT exs_count FROM users WHERE id == ?", (user, )).fetchone()[0]
        self.cur_us.execute("UPDATE users SET exs_count == ? WHERE id == ?", (exs_count+k, user))
        self.db_us.commit()


    def reset_streak(self):
        users = self.get_users()
        for user in users:
            streak = self.cur_us.execute("SELECT streak FROM users WHERE id == ?", (user, )).fetchone()[0]
            if streak == 0:
                self.cur_us.execute("UPDATE users SET days == ? WHERE id == ?", (0, user))
            self.cur_us.execute("UPDATE users SET streak == ? WHERE id == ?", (0, user))
        self.db_us.commit()


    def add_exs(self, exs, n):
        var_id = int(self.cur_us.execute("SELECT data FROM serv WHERE key == ?", ("var_id", )).fetchone()[0])
        ans = []
        if n == -1:
            for i in range(12):
                ans.append(self.cur_ex.execute("SELECT answer FROM exs WHERE id == ?", (f"{i+1}_{exs[i]}", )).fetchone()[0])
        else:
            for i in exs:
                ans.append(self.cur_ex.execute("SELECT answer FROM exs WHERE id == ?", (f"{n}_{i}", )).fetchone()[0])
        ans = "; ".join(ans)
        self.cur_us.execute("INSERT INTO vars VALUES(?, ?)", (var_id, ans))
        self.cur_us.execute("UPDATE serv SET data == ? WHERE key == ?", (var_id + 1, "var_id"))
        self.db_us.commit()
        return var_id
    

    def set_cur_var(self, user, var):
        self.cur_us.execute("UPDATE users SET cur_var == ? WHERE id == ?", (var, user))
        self.db_us.commit()


    def get_answers(self, user):
        cur_var = int(self.cur_us.execute("SELECT cur_var FROM users WHERE id == ?", (user, )).fetchone()[0])
        res = self.cur_us.execute("SELECT answer FROM vars WHERE id == ?", (cur_var, )).fetchone()[0]
        return res
    

    def get_users(self):
        res = [i[0] for i in self.cur_us.execute("SELECT id FROM users").fetchall()]
        return res
    
    
    def add_user(self, user):
        self.cur_us.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)", (user, 0, 0, 100, 0, 1))
        self.db_us.commit()


    def fill_ex(self):
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
    
