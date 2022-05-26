def count_text(val: int, words: list[str]):
    """Слова в __words__ таком порядке: 1 пользователя, 2 пользователя, 5 пользователей"""
    if all((val % 10 == 1, val % 100 != 11)):
        return words[0]
    elif all((2 <= val % 10 <= 4,
              any((val % 100 < 10, val % 100 >= 20)))):
        return words[1]
    return words[2]
