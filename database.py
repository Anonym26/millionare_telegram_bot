import sqlite3
from time import time


# создаем класс пользователей нашего телеграмм бота
class UsersCRUD:  # create read update delete
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        # первый sql-запрос
        self.conn.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        user_id VARCHAR(16) NOT NULL,
        user_name VARCHAR(32) NOT NULL,
        user_ref VARCHAR(16) NOT NULL, 
        sub INT NOT NULL,
        balance INT NOT NULL DEFAULT 10)""")

        # создаем курсор
        self.cursor = self.conn.cursor()

    def __exist_user(self, user_id) -> bool:
        """Проверяет есть ли пользователь в БД"""
        user = self.cursor.execute("""SELECT * FROM users WHERE user_id = ?""", (user_id,)).fetchone()
        return bool(user)

    def __create_user(self, user_id, user_name, user_ref=0, sub_time=0) -> None:
        """Создает пользователя и добавляет в БД"""
        sub_time += int(time())
        self.cursor.execute("""INSERT INTO users (user_id, user_name,user_ref, sub) VALUES (?, ?, ?, ?)""",
                            (user_id, user_name, user_ref, sub_time))
        # фиксируем действие (нужен когда чтото изменили)
        self.conn.commit()

    def add_new_user(self, user_id, user_name, user_ref=0, sub_time=0) -> bool:
        """Добавляет нового пользователя если его нет

        Если пользователь есть возвращает True,
        Если нет то False"""
        if self.__exist_user(user_id):
            return False
        if not (user_ref and self.__exist_user(user_ref)):
            user_ref = 0
        self.__create_user(user_id, user_name, user_ref, sub_time)
        return True

    def count_ref(self, user_id):
        """Считает количество рефералов для конкретного пользователя"""
        count = self.cursor.execute("""SELECT COUNT(user_id) FROM users WHERE user_ref=?""",
                                    (user_id,)).fetchone()
        return count[0]

    def add_balance(self, summa, user_id):
        """После пополнения, добавляет балланс на счет пользователя
        и 10% от суммы пополнения на счет реферала (при наличии) """
        self.cursor.execute("""UPDATE users SET balance = balance + ? WHERE user_id = ?""", (summa, user_id))
        user_ref = self.cursor.execute("""SELECT user_ref FROM users WHERE user_id=?""", (user_id,)).fetchone()
        if user_ref[0]:
            summa_ref = int(int(summa) / 10)
            self.cursor.execute("""UPDATE users SET balance = balance + ? WHERE user_id = ?""",
                                (summa_ref, user_ref[0]))
        self.conn.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.conn.close()