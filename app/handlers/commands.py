from aiogram import types

from app.handlers.quiz import users
from main import dp, bot


# обработчик команды start
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """В ответ на команду start выводит сообщение о начале игры и соответствующую кнопку и обнуляет счетчики вопросов и
     выйгрыша"""
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Начать игру', callback_data='start_quiz'))
    await bot.send_message(chat_id=message.from_user.id,
                           text='Добро пожаловать на игру: "Кто хочет стать милионнером?"\n\n'
                                'Вам необходимо ответить на 15 вопросов, которые разделенны на 4 категории сложности. '
                                'Ответив на все 15 вопросов Вы получите 1 000 000 рублей. Ответив неверно, Вы '
                                'проиграете и останетесь с несгораемой суммой до которой успели дойти.\n',
                           reply_markup=keyboard)

    users.clear()


# обработчик команды help
@dp.message_handler(commands='help')
async def cmd_help(message: types.Message):
    """Выводит клавиатуру с возможными подсказками (если они не использованы)"""
    user_id = str(message.from_user.id)
    if int(users.get(user_id + '_score', 0)):
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        buttons = [
            types.InlineKeyboardButton('50/50', callback_data='50/50'),
            types.InlineKeyboardButton('Помощь зала', callback_data='help_people')
        ]
        keyboard.add(*buttons)
        await bot.send_message(chat_id=message.from_user.id, text='Воспользуйтесь подсказкой', reply_markup=keyboard)


# обработчик команды exit
@dp.message_handler(commands='exit')
async def cmd_exit(message: types.message):
    """В ответ на команду exit обнуляет счетчики вопросов и выйгрыша и завершает игру"""
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    users.clear()
