def winning_amount(balance: int) -> int:
    """Определяет сумму выйгрыша исходя из баланса и списка несгораемых сумм"""
    save_sum = [999, 9999, 99999, 499999, balance]
    save_sum.sort()
    return save_sum[save_sum.index(balance) - 1] + 1 if balance >= 1000 else 0


