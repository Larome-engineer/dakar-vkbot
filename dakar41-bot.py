import re

from func_for_states import *
from keyboard_creators import *
from dictionary import *

from privacy import token
from vkbottle.bot import Bot, Message
from vkbottle import GroupTypes, GroupEventType, VKAPIError, CtxStorage


bot = Bot(token=token)
bot.labeler.vbml_ignore_case = True


@bot.on.private_message(text=["верно", "не верно"])
async def check_handler(msg: Message):
    await checker(msg)


@bot.on.private_message(text=hello_words_list)
async def greetings_handler(msg: Message):
    user = await bot.api.users.get(msg.from_id)
    await msg.answer(f"Здравствуйте, {user[0].first_name}! 👋🏻")
    await msg.answer("Меня зовут Dak. Я онлайн-консультант магазина Dakar41 🤖")
    await options_keyboard(msg=msg)


@bot.on.private_message(text=gratitude_list)
async def gratitude_handler(msg: Message):
    await msg.answer("Пожалуйста! Приезжайте к нам чаще!\n"
                     "Всегда рады заботиться о ваших машинках!🔥")


@bot.on.private_message(text="меню")
async def menu_handler(msg: Message):
    await options_keyboard(msg=msg)


@bot.on.private_message(text="Каталог")
async def link_handler(msg: Message):
    await links_keyboard(msg=msg)


@bot.on.private_message(text="Адрес")
async def address_handler(msg: Message):
    await msg.answer(f"🏪 Наш адрес:\n{address}\n\nРаботаем круглосуточно 🔧")
    await create_route_keyboard(msg=msg)


@bot.on.private_message(text=["да", "нет"])
async def route_handler(msg: Message):
    if msg.text == "Да":
        await route_keyboard(msg=msg)
    elif msg.text == "Нет":
        await options_keyboard(msg)


@bot.on.private_message(text="Контакты")
async def contact_handler(msg: Message):
    await contacts_keyboard(msg=msg)


@bot.on.private_message(text="Доп.информация")
async def info_handler(msg: Message):
    await msg.answer(f"📦 Доставка и оплата 📦\n\n{delivery_pay_txt}")


@bot.on.private_message(text="Оставить заявку")
async def reg_handler(msg: Message):
    await msg.answer("📄 Оформление заявки\n\nВведите следущие параметры:\n\n"
                     "Параметры шины в такой последовательности:\n\n"
                     "1⃣ Ширина профиля\n2⃣ Высота профиля\n3⃣ Посадочный диаметр\n\n"
                     "Пример сообщения:\n'225/45/R17'\n\n"
                     
                     "©️ Введите марку шины\n(по желанию)\n\n"
                     "Пример:\n'Bridgestone' или 'BFGoodrich'\n\n"
                     "Если нет определенного ответа, то напишите '-'"
                     
                     "Введите количество шин (по желанию)\n\n" 
                     "Пример: '2' или '4'\n\n" 
                     "Если нет определенного ответа, то отправьте '-'\n\n"
                     
                     "♻ Введите желаемое состояние товара:\n\n"
                     "Пример: 'Новое' или 'Б/У'\n\n"
                     
                     "📆 Введите желаемый протектор (сезон):\n\n"
                     "Пример: 'Летняя' 'Зимняя' 'Грязь АТ' 'Грязь МТ'\n\n"
                     
                     "⚙ В желаемый параметр шиповки")


@bot.on.private_message(text=bad_words_list)
async def bad_handler(msg: Message):
    await msg.answer(f"Ну что же Вы так сразу... \n"
                     f"Не выражайтесь! Мы ценим манеры ☝🏻\n\n"
                     f"Отправьте нам слово 'Привет' для начала диалога")


@bot.on.private_message()
async def confused(msg: Message):
    await msg.answer("Я Вас не понимаю.\nОтправьте слово 'Привет' для начала работы или 'Меню' "
                     "для быстрого перехода в главное меню")


@bot.on.raw_event(GroupEventType.GROUP_JOIN, dataclass=GroupTypes.GroupJoin)
async def group_join_handler(event: GroupTypes.GroupJoin):
    try:
        await bot.api.messages.send(
            peer_id=event.object.user_id,
            message="Благодарим за подписку! 🔥\n\nДля начала работы поздоровайтесь "
                    "с нашим онлайн-консультантом, отправив сообщение: 'Привет'",
            random_id=0
        )
    except VKAPIError[901]:
        pass


@bot.on.raw_event(GroupEventType.GROUP_LEAVE, dataclass=GroupTypes.GroupLeave)
async def group_join_handler(event: GroupTypes.GroupLeave):
    try:
        await bot.api.messages.send(
            peer_id=event.object.user_id,
            message="Нам жаль, что Вы отписывайтесь... 😞\n"
                    "Будем ждать Вас снова, чтобы информировать о новинках!\n\n"
                    "Наш онлайн-консультант по-прежнему доступен для Вас! 🤖",
            random_id=0
        )
    except VKAPIError[901]:
        pass


bot.run_forever()
