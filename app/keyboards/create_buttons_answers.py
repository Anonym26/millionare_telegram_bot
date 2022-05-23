from aiogram import types


def create_buttons(next_question):
    """Создает список с кнопками-ответами """
    question = list(next_question[1].keys())
    answer = list(next_question[1].values())
    buttons = [
        types.InlineKeyboardButton(question[0], callback_data=answer[0]),
        types.InlineKeyboardButton(question[1], callback_data=answer[1]),
        types.InlineKeyboardButton(question[2], callback_data=answer[2]),
        types.InlineKeyboardButton(question[3], callback_data=answer[3])
    ]
    return buttons


def create_buttons_fifty(dict_answers: dict):
    """Создает список с кнопками-ответами при активации подсказки 50/50"""
    question = list(dict_answers.keys())
    answer = list(dict_answers.values())
    buttons = [
        types.InlineKeyboardButton(question[0], callback_data=answer[0]),
        types.InlineKeyboardButton(question[1], callback_data=answer[1])
    ]
    return buttons
