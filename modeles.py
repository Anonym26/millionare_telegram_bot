from time import time
from app.utility.text_end import count_text


# создаем класс-модель пользователя


class User:
    def __init__(self, user_data: tuple):
        self.id = user_data[0]
        self.user_id = user_data[1]
        self.name = user_data[2]
        self.ref = user_data[3]
        self.sub = user_data[4]
        self.balance = user_data[5]

    def __repr__(self):
        return "<User(id: %s, user_id: %s, name: %s)>" % (self.id, self.user_id, self.name)

    def check_sub(self) -> bool:
        """Возвращает True если время подписки еще не истекло"""
        return time() < self.sub

    def update_sub(self, upd_time: int):
        """Добавляет время подписки"""
        if self.check_sub():
            self.sub += upd_time
        else:
            self.sub = int(time()) + upd_time

    @staticmethod
    def __calc_price(days: int) -> int:
        """Расчитывает стоимость подписки"""
        if days < 1:
            raise Exception('invalid')
        elif days < 7:
            return days * 20
        elif days < 14:
            return days * 18
        elif days < 30:
            return days * 15
        else:
            return days * 10

    def buy_sub(self, days: int) -> bool:
        """Вернет False если нет денег, если все ок вернет True"""
        price_sub = self.__calc_price(days)
        if self.balance >= price_sub:
            self.balance -= price_sub
            self.update_sub(days * 24 * 60 * 60)
            return True
        return False

    def dict(self):
        return self.__dict__

    def get_sub_time_text(self):
        """Выводит информацию о статусе подписки:
        - либо закончилась;
        - либо сколько осталось"""
        if not self.check_sub():
            return 'Ваша подписка закончилась'
        s_time = self.sub - int(time())
        days = s_time // (3600 * 24)
        hours = (s_time - (days * 3600 * 24)) // 3600

        if s_time > 24 * 3600:
            return f'Осталось {days} {count_text(days, ["день", "дня", "дней"])} ' \
                   f'{hours} {count_text(hours, ["час", "часа", "часов"])}'
