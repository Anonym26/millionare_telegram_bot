def calc_price(days: int) -> int:
    """Расчитывает стоимость подписки"""
    if days < 1:
        return 0
    elif days < 7:
        return days * 20
    elif days < 14:
        return days * 18
    elif days < 30:
        return days * 15
    else:
        return days * 10
