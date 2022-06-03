from aiogram import types
from aiogram.dispatcher.filters import Text

from app.utility.calc_price_sub import calc_price
from main import dp, users_db

user_data = {}


def get_keyboard():
    """Генерация клавиатуры"""
    buttons = [
        types.InlineKeyboardButton(text='-1', callback_data='num_decr'),
        types.InlineKeyboardButton(text='+1', callback_data='num_incr'),
        types.InlineKeyboardButton(text='Подтвердить', callback_data='num_finish')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


async def update_num_text(message: types.Message, new_value: int, user_value: int):
    """Общая функци для обновления текста с отправкой той же клавиатуры"""
    price = calc_price(user_value)
    await message.edit_text(f'Покупка подписки\n'
                            f'Количество дней: {new_value} '
                            f'Цена: {price}\n',
                            reply_markup=get_keyboard())


@dp.message_handler(commands='buy_sub')
async def cmd_numbers(message: types.Message):
    """Функция вывода клавиатуры по команде buy_sub"""
    user_data[message.from_user.id] = 0
    await message.answer('Покупка подписки\n'
                         'Количество дней: 0 '
                         'Цена: 0\n',
                         reply_markup=get_keyboard())


@dp.callback_query_handler(Text(startswith='num_'))
async def callbacks_num(call: types.CallbackQuery):
    """Получаем текущее значение для пользователя, либо считаем его равным 0"""
    user_value = user_data.get(call.from_user.id, 0)
    action = call.data.split('_')[1]
    if action == 'incr':
        user_data[call.from_user.id] = user_value + 1
        await update_num_text(call.message, user_value + 1, user_value + 1)
    elif action == 'decr':
        if user_value:
            user_data[call.from_user.id] = user_value - 1
            await update_num_text(call.message, user_value - 1, user_value - 1)
    elif action == 'finish':
        user_id = call.from_user.id
        user = users_db.get_user_by_user_id(user_id)
        sub = user.buy_sub(user_value)
        if sub:
            users_db.update_user(user)
            await call.message.edit_text('Подписка оформлена!')
        else:
            await call.message.edit_text('Недостаточно средств!')
    await call.answer()
