from core.config import settings
from core.load import get_bot

_BOT = get_bot()


async def send_order_to_group(name: str, phone_num: str, order: list):
    group_id = int(settings.admin_group.chat_id)

    msg = (
        "📦 <b>Buyurtma.</b>\n"
        f"  🪪 <b>Buyurtmachi ismi / Имя заказчика:</b> {name}\n"
        f"  ☎️ <b>Buyurtmachi telefon raqami / Номер телефона заказчика:</b> {phone_num}\n\n"
        "🛒 <b>Buyurtma qiling mahsulotlar:</b>\n"
    )

    total = 0
    for product in order:
        msg += f"   <b>Mahsulot ID:</b> {product['id']}\n"
        msg += f"   <b>Mahsulot nomi:</b> {product['name']}\n"
        msg += f"   <b>Mahsulot narxi:</b> {product['price']}\n"
        msg += f"   <b>Mahsulot SKU:</b> {product['sku']}\n"
        msg += f"   <b>Mahsulotlar soni:</b> {product['count']}\n"
        t = int(product["count"]) * int(product["price"])
        msg += f"   <b>Jami narxi:</b> {t}\n\n"

        total += t
    msg += f"<b>Ummumiy narx / Общая сумма:</b> {total}"

    await _BOT.send_message(chat_id=group_id, text=msg)
