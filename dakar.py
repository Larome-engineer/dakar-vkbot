import re

from privacy import *
from dictionary import *
from func_for_states import *
from keyboard_creators import *
from var_for_states_func import *

from vkbottle.bot import Bot
from vkbottle import BaseStateGroup
from vkbottle import GroupTypes, GroupEventType, VKAPIError

user_dict = {}
order_dict = []

bot = Bot(token=token)
bot.labeler.vbml_ignore_case = True


class User:

    def __init__(self, size):
        self.size = size

        keys = [
            'size', 'brand', 'state', 'season', 'studded',
            'type', 'tire_number', 'number'
        ]

        for key in keys:
            self.key = None


class RegData(BaseStateGroup):
    SIZE = 0
    BRAND = 1
    STATE = 2
    SEASON = 3
    STUDDED = 4
    TYPE = 5
    NUM = 6
    PHONE = 7
    USERNAME = 8
    END = 9


@bot.on.private_message(text=["верно", "неверно"])
async def check_answer_of_order(msg: Message):   # Проверка на корректность и очищение переменных ctx
    if msg.text == "Верно":
        menu = (
            Keyboard(inline=True)
            .add(Text("Меню"), KeyboardButtonColor.PRIMARY)
        )
        await msg.answer("✅ Отлично. Ваша заявка обработана. Через некоторое время мы Вам перезвоним!\n\n"
                         "Нажмите 'Меню', чтобы вернуться в главное меню", keyboard=menu)

    elif msg.text == "Неверно":
        keyboard = (
            Keyboard(inline=True)
            .add(Text("Переоформить заявку"), KeyboardButtonColor.POSITIVE)
        )
        order_dict.pop(-1)
        await msg.answer("Пожалуйста, заполните заявку заново", keyboard=keyboard)


@bot.on.private_message(text=hello_words_list)
async def greetings_handler(msg: Message):
    user = await bot.api.users.get(msg.from_id)
    await msg.answer(f"Здравствуйте, {user[0].first_name}! 👋🏻")
    await msg.answer("Меня зовут Dak. Я онлайн-консультант магазина Dakar41 🤖")
    await options_keyboard(msg=msg)


@bot.on.private_message(text=gratitude_list)
async def gratitude_handler(msg: Message):
    menu = (
        Keyboard(inline=True)
        .add(Text("Меню"), KeyboardButtonColor.PRIMARY)
    )
    await msg.answer("Пожалуйста! Приезжайте к нам чаще!\n"
                     "Всегда рады заботиться о ваших машинках!🔥\n\n"
                     "Можете перейти в раздел меню", keyboard=menu)


@bot.on.private_message(text="Меню")
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


@bot.on.private_message(lev=["Оставить заявку", "Переоформить заявку"])
async def start_order_handler(msg: Message):
    await bot.state_dispenser.set(msg.peer_id, RegData.SIZE)
    return for_size_input


@bot.on.private_message(state=RegData.SIZE)
async def tire_size_handler(msg: Message):
    user = user_dict[msg.from_id] = User(msg.text)
    user.size = msg.text

    await bot.state_dispenser.set(msg.peer_id, RegData.BRAND)
    return for_brand_input


@bot.on.private_message(state=RegData.BRAND)
async def tire_brand_handler(msg: Message):
    user = user_dict[msg.from_id]
    user.brand = msg.text

    await bot.state_dispenser.set(msg.peer_id, RegData.STATE)
    await bus_condition_keyboard(msg)


@bot.on.private_message(state=RegData.STATE)
async def tire_state_handler(msg: Message):
    if msg.text == "Б/У" or msg.text == "Новое":
        user = user_dict[msg.from_id]
        user.state = msg.text

        await bot.state_dispenser.set(msg.peer_id, RegData.SEASON)
        await tire_season_keyboard(msg)
    else:
        await msg.answer("Выберите корректный параметр из выше представленных")


@bot.on.private_message(state=RegData.SEASON)
async def tire_season_handler(msg: Message):
    if msg.text == "Летняя":
        user = user_dict[msg.from_id]
        user.season = msg.text

        await bot.state_dispenser.set(msg.peer_id, RegData.TYPE)
        user.studded = "Без шипов"

        await tire_type_keyboard(msg)
    elif msg.text == "Зимняя" or msg.text == "Грязь МТ" or msg.text == "Грязь АТ":
        user = user_dict[msg.from_id]
        user.season = msg.text

        await bot.state_dispenser.set(msg.peer_id, RegData.STUDDED)
        await tire_studding_keyboard(msg)
    else:
        await msg.answer("Выберите корректный параметр из выше представленных")


@bot.on.private_message(state=RegData.STUDDED)
async def tire_std_handler(msg: Message):
    if msg.text == "Шипы" or msg.text == "Без шипов":
        user = user_dict[msg.from_id]
        user.studded = msg.text

        await bot.state_dispenser.set(msg.peer_id, RegData.TYPE)
        await tire_type_keyboard(msg)
    else:
        await msg.answer("Выберите корректный параметр из выше представленных.")


@bot.on.private_message(state=RegData.TYPE)
async def tire_type_handler(msg: Message):
    if msg.text == "Обычная" or msg.text == "Грузовая и LT":
        user = user_dict[msg.from_id]
        user.type = msg.text

        await bot.state_dispenser.set(msg.peer_id, RegData.NUM)
        num = (
            Keyboard(inline=True)
            .add(Text("1"), KeyboardButtonColor.PRIMARY)
            .add(Text("2"), KeyboardButtonColor.PRIMARY).row()
            .add(Text("3"), KeyboardButtonColor.PRIMARY)
            .add(Text("4"), KeyboardButtonColor.PRIMARY)
        )
        await msg.answer("Выберите нужное количество шин", keyboard=num)

    else:
        await msg.answer("Выберите корректный параметр из выше представленных.")


@bot.on.private_message(state=RegData.NUM)
async def tire_num_handler(msg: Message):
    user = user_dict[msg.from_id]
    user.tire_number = msg.text

    await bot.state_dispenser.set(msg.peer_id, RegData.PHONE)
    return for_contact_input


@bot.on.private_message(state=RegData.PHONE)
async def client_phone_handler(msg: Message):
    pattern = '[-()]'
    num = msg.text
    num = (re.sub(pattern, '', num.replace('+7', '8')))

    user = user_dict[msg.from_id]
    user.number = num

    await bot.state_dispenser.set(msg.peer_id, RegData.USERNAME)
    return "Как мы можем официально к Вам обращаться?"


@bot.on.private_message(state=RegData.USERNAME)
async def client_name_handler(msg: Message):
    chat_id = msg.from_id
    user = user_dict[chat_id]
    user.name = msg.text

    await bot.state_dispenser.set(msg.peer_id, RegData.END)
    await check_of_correct(msg)


@bot.on.private_message(state=RegData.END, text="Проверить заявку")
async def client_name_handler(msg: Message):
    chat_id = msg.from_id
    user = user_dict[chat_id]

    size = user.size
    brand = user.brand
    state = user.state
    season = user.season
    std = user.studded
    types = user.type
    tire_number = user.tire_number
    name = user.name
    number = user.number

    message = "🔤 Параметры шины:\n>>>> " + size + "\n\n"\
              "©️ Марка шины:\n>>>> " + brand + "\n\n"\
              "♻ Состояние:\n>>>> " + state + "\n\n"\
              "📆 Протектор (сезон):\n>>>> " + season + "\n\n"\
              "⚙ Шиповка:\n>>>> " + std + "\n\n"\
              "🚜 Тип шины:\n>>>> " + types + "\n\n"\
              "🔢 Количество: " + tire_number + "\n\n"\
              "Ваше имя: " + name + "\n"\
              "Ваш номер: " + number

    order_dict.append(message)

    await msg.answer("📋 ВАША ЗАЯВКА\n\n" + message)

    await answer_keyboard(msg)
    await check_answer_of_order(msg)


@bot.on.private_message(text=bad_words_list)
async def bad_words_check(msg: Message):
    await msg.answer("Ну что же Вы так сразу... \n"
                     "Не выражайтесь! Мы ценим манеры ☝🏻\n\n"
                     "Отправьте нам слово 'Привет' для начала диалога или слово 'Меню' для перехода в главное меню.")


@bot.on.chat_message(text="/check")
async def chat_check_handler(msg: Message):
    i = 0
    if order_dict:
        for m in order_dict:
            i += 1
            await msg.answer(f"📋 ЗАЯВКА: {i}\n\n" + m)
    else:
        await msg.answer("Нет новых заявок")


@bot.on.chat_message(text="/delete")
async def chat_delete_handler(msg: Message):
    order_dict.clear()
    await msg.answer("Все заявки удалены")


@bot.on.private_message()
async def confused(msg: Message):
    await msg.answer("Я Вас не понимаю.\nОтправьте слово 'Привет' для начала работы или 'Меню' "
                     "для быстрого перехода в главное меню.")


@bot.on.raw_event(GroupEventType.GROUP_JOIN, dataclass=GroupTypes.GroupJoin)
async def group_join_handler(event: GroupTypes.GroupJoin):
    try:
        await bot.api.messages.send(
            peer_id=event.object.user_id,
            message="Благодарим за подписку! 🔥\n\nДля начала работы поздоровайтесь "
                    "с нашим онлайн-консультантом, отправив сообщение: 'Привет'.",
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
