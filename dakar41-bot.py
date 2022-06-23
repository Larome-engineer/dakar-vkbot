import re

from func_for_states import *
from keyboard_creators import *
from dictionary import *

from privacy import token
from vkbottle.bot import Bot, Message
from vkbottle import GroupTypes, GroupEventType, VKAPIError, CtxStorage
from vkbottle import BaseStateGroup

ctx = CtxStorage()
bot = Bot(token=token)
bot.labeler.vbml_ignore_case = True


class RegData(BaseStateGroup):
    SIZE = 0
    BRAND = 1
    STATE = 2
    SEASON = 3
    STUDDED = 4
    TYPE = 5
    PHONE = 6
    USERNAME = 7


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


@bot.on.private_message(lev="Оставить заявку")
async def reg_handler(msg: Message):
    await bot.state_dispenser.set(msg.peer_id, RegData.SIZE)
    return about_size


@bot.on.private_message(state=RegData.SIZE)
async def size_handler(msg: Message):
    ctx.set("size", msg.text)
    await bot.state_dispenser.set(msg.peer_id, RegData.BRAND, something=1)
    return about_brand


@bot.on.private_message(state=RegData.BRAND)
async def brand_handler(msg: Message):
    ctx.set("brand", msg.text)
    await bot.state_dispenser.set(msg.peer_id, RegData.STATE)
    state = await bus_condition(msg)
    return state


@bot.on.private_message(state=RegData.STATE)
async def state_handler(msg: Message):
    if msg.text == "Б/У" or msg.text == "Новое":
        ctx.set("state", msg.text)
        await bot.state_dispenser.set(msg.peer_id, RegData.SEASON)
        season = await tire_season(msg)
        return season
    else:
        await msg.answer("Выберите корректный параметр из выше представленных")


@bot.on.private_message(state=RegData.SEASON)
async def season_handler(msg: Message):
    if msg.text == "Летняя" or msg.text == "Зимняя" or msg.text == "Грязь МТ" or msg.text == "Грязь АТ":
        ctx.set("season", msg.text)
        await bot.state_dispenser.set(msg.peer_id, RegData.STUDDED)
        studded = await tire_studding(msg)
        return studded
    else:
        await msg.answer("Выберите корректный параметр из выше представленных")


@bot.on.private_message(state=RegData.STUDDED)
async def std_handler(msg: Message):
    if msg.text == "Шипы" or msg.text == "Без шипов":
        ctx.set("studded", msg.text)
        await bot.state_dispenser.set(msg.peer_id, RegData.TYPE)
        types = await tire_type(msg)
        return types
    else:
        await msg.answer("Выберите корректный параметр из выше представленных")


@bot.on.private_message(state=RegData.TYPE)
async def phone_handler(msg: Message):
    if msg.text == "Обычная" or msg.text == "Грузовая и LT":
        ctx.set("type", msg.text)
        await bot.state_dispenser.set(msg.peer_id, RegData.PHONE)
        return about_contact
    else:
        await msg.answer("Выберите корректный параметр из выше представленных")


@bot.on.private_message(state=RegData.PHONE)
async def phone_handler(msg: Message):
    pattern = '[-()]'
    num = msg.text
    num = (re.sub(pattern, '', num.replace('+7', '8')))
    ctx.set("phone", num)
    await bot.state_dispenser.set(msg.peer_id, RegData.USERNAME)
    return "Как мы можем официально к Вам обращаться?"


@bot.on.private_message(state=RegData.USERNAME)
async def type_handler(msg: Message):
    size = ctx.get("size")
    brand = ctx.get("brand")
    state = ctx.get("state")
    season = ctx.get("season")
    studded = ctx.get("studded")
    typing = ctx.get("type")
    number = ctx.get("phone")
    name = msg.text

    await msg.answer(f"Проверьте, верно ли Вы ввели все параметры:\n\n"
                     f"🔤 Параметры шины: {size}\n\n"
                     f"©️ Марка шины: {brand}\n\n"
                     f"♻ Состояние: {state}\n\n"
                     f"📆 Протектор (сезон): {season}\n\n"
                     f"⚙ Шиповка: {studded}\n\n"
                     f"🚜 Тип шины: {typing}\n\n"
                     f"Ваше имя: {name}\n"
                     f"Ваш номер: {number}")

    await answer_keyboard(msg)
    await check_handler(msg)


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
