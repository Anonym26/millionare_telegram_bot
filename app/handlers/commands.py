from aiogram import types

from app.handlers.quiz import users
from app.utility.text_end import count_text
from main import dp, bot, users_db


# обработчик команды start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """В ответ на команду start выводит сообщение о начале игры
    и соответствующую кнопку и обнуляет счетчики вопросов
    и выйгрыша"""
    await message.delete()
    user_ref = 0 if len(message.text.split()) < 2 else message.text.split()[1]

    try:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    except Exception as Ex:
        print(f'{Ex}. Работаем дальше.')

    if users_db.add_new_user(user_id=message.from_user.id,
                             user_name=message.from_user.first_name,
                             user_ref=user_ref):
        await message.answer("Опа, новенький!\nДержи 10 приветственных коинов!")
    else:
        await message.answer("И снова здраствуйте!")

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Начать игру', callback_data='start_quiz'))

    await bot.send_message(chat_id=message.from_user.id,
                           text='Добро пожаловать на игру: "Кто хочет стать милионнером?"\n\n'
                                'Вам необходимо ответить на 15 вопросов, которые разделенны на 4 категории '
                                'сложности. '
                                'Ответив на все 15 вопросов Вы получите 1 000 000 рублей. Ответив неверно, Вы '
                                'проиграете и останетесь с несгораемой суммой до которой успели дойти.\n',
                           reply_markup=keyboard)
    users.clear()


# обработчик команды help
@dp.message_handler(commands='help')
async def cmd_help(message: types.Message):
    """Выводит клавиатуру с возможными подсказками (если они не использованы)"""
    await message.delete()
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
async def cmd_exit(message: types.Message):
    """В ответ на команду exit обнуляет счетчики вопросов и выйгрыша и завершает игру"""
    await message.delete()
    try:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    except Exception as Ex:
        print(f'{Ex}. Работаем дальше.')
    finally:
        users.clear()


# реферальная ссылка
@dp.message_handler(commands=['ref'])
async def ref_funk(message: types.Message):
    """Формирует реферальную ссылку для пользователя вызвавшего метод"""
    await message.delete()
    count_users = users_db.count_ref(message.from_user.id)
    refs = f'Вы пригласили {count_users} пользовател' + count_text(count_users, ['я', 'eй', 'ей'])
    link = 'https://t.me/imsr_su_bot?start=' + str(message.from_user.id)
    return await message.answer(refs + '\nВаша реф ссылка: ' + link)


@dp.message_handler(commands=['balance'])
async def show_balance(message: types.Message):
    """Показывает баланс пользователя"""
    await message.delete()
    user_id = message.from_user.id
    user = users_db.get_user_by_user_id(user_id).balance
    return await message.answer(f"Ваш баланс: {user} кои" + count_text(user, ['н', 'на', 'нов']))


@dp.message_handler(commands=['status_sub'])
async def cmd_status_sub(message: types.Message):
    """Показывает статус подписки"""
    await message.delete()
    user_id = message.from_user.id
    user = users_db.get_user_by_user_id(user_id).get_sub_time_text()
    return await message.answer(user)
