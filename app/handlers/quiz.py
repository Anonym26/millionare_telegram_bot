from aiogram import types

from app.keyboards.create_buttons_answers import create_buttons
from app.utility.get_questions import get_question
from app.utility.show_correct_answer import show_correct_answer
from app.utility.winning_amount import winning_amount
from config import apikey
from main import dp, bot

users = {
    'user_id_score': 'count_question',
    'user_id_balance': 'balance',
    'user_id_hints': ['50/50', 'help_people'],
    'user_id_question': ('question', ['answers'])
}
win_sum = [100, 500, 1000, 5000, 10000, 50000, 100000, 200000, 300000, 500000, 600000, 700000, 800000, 9000000,
           10000000]


@dp.callback_query_handler(text='start_quiz')
async def send_nest_question(call: types.CallbackQuery):
    """Используя функцию get_question получает первый вопрос и список ответов и выводит на экран"""
    await call.message.delete_reply_markup()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    user_id = str(call.from_user.id)
    question = users.setdefault(user_id + '_score', 1)
    users.update({user_id + '_hints': ['50/50', 'help_people']})
    next_question = get_question(question, apikey)
    users.update({user_id + '_question': next_question})

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = create_buttons(next_question)
    keyboard.add(*list(buttons))

    await bot.send_message(chat_id=call.from_user.id, text=f'Вопрос № {question}\n\n{next_question[0]}',
                           reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text='correct_answer')
async def send_next_question(call: types.CallbackQuery):
    """Используя функцию get_question получает вопрос и список ответов и выводит на экран"""
    await call.message.delete_reply_markup()

    user_id = str(call.from_user.id)
    question = int(users.get(user_id + '_score', 0))
    balance = users.setdefault(user_id + '_balance', win_sum[0])
    if question <= 14:
        await call.answer(text=f'Поздравляем!\nВы выйграли {balance} рублей!', show_alert=True)
        users[user_id + '_balance'] = win_sum[question]
        users[user_id + '_score'] += 1

        next_question = get_question(question, apikey)
        users.update({user_id + '_question': next_question})

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        buttons = create_buttons(next_question)
        keyboard.add(*list(buttons))

        await bot.send_message(chat_id=call.from_user.id, text=f'Вопрос № {question + 1}\n\n{next_question[0]}',
                               reply_markup=keyboard)
    elif question == 15:
        await call.answer(text='Ура, победа!\n Вы выйграли 1 миллион рублей!\n🥳', show_alert=True)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.answer()


@dp.callback_query_handler(text='incorrect_answer')
async def finish(call: types.CallbackQuery):
    """При неправильном ответе выводит всплывающее сообщение о пройгрыше, правильном ответе и выйгранной сумме"""
    user_id = str(call.from_user.id)
    balance = users.setdefault(user_id + '_balance', 0)
    result = dict(call.message['reply_markup'])
    list_answer = result['inline_keyboard'][0] + result['inline_keyboard'][1]
    await call.answer(text=f'Вы проиграли :(\n'
                           f'Правильный ответ: {show_correct_answer(list_answer)}\n '
                           f'Ваш выйгрыш составил {winning_amount(balance)} рублей.', show_alert=True)

    await call.message.delete_reply_markup()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.answer()
