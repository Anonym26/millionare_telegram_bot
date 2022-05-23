from random import randint

from aiogram import types

from app.handlers.quiz import users
from app.keyboards.create_buttons_answers import create_buttons_fifty
from app.utility.show_correct_answer import show_two_answers, show_answers_help_people
from main import dp, bot


@dp.callback_query_handler(text='50/50')
async def hints_50_50(call: types.CallbackQuery):
    """Реализует подсказку 50/50 оставляя два варианта ответа путем изменения сообщения с вопросом
    и клавиатурой-ответами"""
    user_id = str(call.from_user.id)
    if users[f'{user_id}_hints'].count('50/50'):
        users[f'{user_id}_hints'].remove('50/50')
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        count_question = users[user_id + '_score']
        question = users[f'{user_id}_question'][0]
        keyboard = types.InlineKeyboardMarkup()
        answers = list(users[f'{user_id}_question'])
        list_answer = show_two_answers(answers[1])
        buttons = create_buttons_fifty(list_answer)
        keyboard.add(*list(buttons))
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id - 2,
                                    text=f'Вопрос № {count_question}\n\n{question}', reply_markup=keyboard)

    else:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await call.answer(text='Подсказка уже использована!', show_alert=True)


@dp.callback_query_handler(text='help_people')
async def hints_help_people(call: types.CallbackQuery):
    """Реализует подсказку help_people оставляя правильный вариант ответа"""
    user_id = str(call.from_user.id)
    if users[f'{user_id}_hints'].count('help_people'):
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
        users[f'{user_id}_hints'].remove('help_people')
        people = randint(50, 100)
        answers = list(users[f'{user_id}_question'])
        await call.answer(text=f'{people} % людей считает, что правильный ответ:\n\n'
                               f'{show_answers_help_people(answers[1])}', show_alert=True)
    else:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await call.answer(text='Подсказка уже использована!', show_alert=True)