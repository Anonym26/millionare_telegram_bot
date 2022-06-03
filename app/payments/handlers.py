from main import bot, anti_flood, dp, users_db
from aiogram import types
from config import payments_token


async def send_offer(user_id, price: int):
    await bot.send_invoice(user_id,
                           title='{} рублей'.format(price),
                           description='Пополнение баланса на {} рублей'.format(price),
                           provider_token=payments_token,
                           currency='RUB',
                           is_flexible=False,  # True если конечная цена зависит от способа доставки
                           prices=[types.LabeledPrice(label='{} рублей'.format(price), amount=price * 100)],
                           start_parameter='time-machine-example',
                           payload=price
                           )


@dp.message_handler(commands=['get_offer'])
@dp.throttled(anti_flood, rate=1)
async def get_offer(message: types.Message):
    user_id = message.from_user.id
    return await send_offer(user_id, 100)


# нужно чтобы удостоверилась что платежная система фурычит
@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    return await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    invoice_payload = message.successful_payment.to_python()['invoice_payload']

    user_id = message.from_user.id
    user = users_db.get_user_by_user_id(user_id)
    user.balance += int(invoice_payload)
    users_db.update_user(user)

    user_id_ref = user.ref
    user_ref = users_db.get_user_by_user_id(user_id_ref)
    user_ref.balance += int(int(invoice_payload) / 10)
    users_db.update_user(user_ref)

    return
