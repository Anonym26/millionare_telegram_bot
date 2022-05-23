def show_correct_answer(list_answers: list) -> str:
    """Принимает список словарей {ответ, статус ответа} и возвращает правильный ответ"""
    answer = next(x for x in list_answers if x["callback_data"] == "correct_answer")
    return answer['text']


def show_two_answers(list_answers: list) -> dict:
    """Принимает список словарей {ответ, статус ответа} и возвращает правильный ответ и один неправильный"""
    answers = {}
    for i in list_answers:
        if list_answers[i] == "correct_answer":
            answers.update({i: list_answers[i]})
            break
    for j in list_answers:
        if list_answers[j] == "incorrect_answer":
            answers.update({j: list_answers[j]})
            break

    return answers


def show_answers_help_people(list_answers: list) -> dict:
    """Принимает список словарей {ответ, статус ответа} и возвращает правильный ответ"""
    for i in list_answers:
        if list_answers[i] == "correct_answer":
            return i
