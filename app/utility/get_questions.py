import random

import requests
from fake_useragent import UserAgent


# функция создания словаря с ответами
def create_dict_answers(answers: list) -> dict:
    """Принимает список и создает из него словарь, где ключ - это элемент списка, а значение correct_answer у первого
    и incorrect_answer у остальных"""
    dict_answers = {}
    for v, i in enumerate(answers):
        if v == 0:
            dict_answers.update({i: 'correct_answer'})
        else:
            dict_answers.update({i: 'incorrect_answer'})
    return dict_answers


# функция перемешивания словаря
def shuffle_dict_answers(dict_answers: dict) -> dict:
    """Принимает словарь и возвращает перемешанных словарь"""
    dict_answers_item = list(dict_answers.items())
    random.shuffle(dict_answers_item)
    dict_answers = dict(dict_answers_item)
    return dict_answers


session = requests.session()
ua = UserAgent()
count_amount = 17


# функция получения вопроса и ответов
def get_question(question: int, api_key: str, count: int = 1):
    """Принимает параметры: уровень сложности (от 1 до 4) и число вопросов (от 1 до 5),
    отправляет запрос и получает вопросы с вариантами ответа (1 вариант всегда правильный). Возвращает кортеж из вопроса
    и словаря {ответ: """
    global count_amount
    if question <= 3:
        difficulty_level = 4
    elif 3 < question <= 7:
        difficulty_level = 1
    elif 7 < question <= 12:
        difficulty_level = 2
    else:
        difficulty_level = 3

    # для запросов с api ключем
    # link = f'https://engine.lifeis.porn/api/millionaire.php?qType={difficulty_level}&count={count}' \
    #    f'&apikey={api_key}'
    # amount = responce['amount']
    # print(f'Осталось запросов: {int(float(amount) / 0.02)}')

    link = f'https://engine.lifeis.porn/api/millionaire.php?qType={difficulty_level}&count={count}'
    headers = {'User_Agent': ua.random}
    responce = session.get(link, headers=headers).json()

    question = str(responce['data'][0]['question']).replace('\u2063', '')
    answers = responce['data'][0]['answers']
    dict_answers = create_dict_answers(answers)
    dict_answers_shuffle = shuffle_dict_answers(dict_answers)
    return question, dict_answers_shuffle

# print(get_question(1, '42ed114383baff234bfb5bd92'))
