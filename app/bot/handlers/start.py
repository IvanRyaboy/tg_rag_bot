from aiogram.filters import CommandStart
from aiogram.types import Message
from app.bot.dispatcher import dp
import logging


log = logging.getLogger("tg-webhook")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    log.info(
        "Start from user_id=%s, name=%s, username=%s",
        message.from_user.id if message.from_user else None,
        message.from_user.full_name if message.from_user else None,
        message.from_user.username if message.from_user else None,
    )
    await message.answer("""
    Здравствуйте. Я — виртуальный риэлтор.
    Помогу найти квартиру для покупки или аренды, рассчитать цену за м² и сравнить варианты по заданным параметрам.
        
    Вы можете задать запрос в свободной форме, например:
    • Квартиры на продажу в Минске до 150 000 $
    • Аренда 2-комнатной квартиры в центре Гродно
    • Посчитай цену за м² у квартиры
    • Сравни две квартиры по адресу … и …
    
    Фильтры указываются прямо в сообщении: город, тип сделки, цена, комнаты и другие параметры.
    Чтобы начать — просто введите ваш запрос.""")
