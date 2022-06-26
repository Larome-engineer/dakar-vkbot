# .py файл для создания отдельных клавиатур

from privacy import phone
from useful_links import *
from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink


async def options_keyboard(msg: Message):  # Клавиатура для главного меню
    keyboard = (
        Keyboard(inline=True)
        .add(Text("Каталог"), KeyboardButtonColor.PRIMARY)
        .add(Text("Адрес"), KeyboardButtonColor.PRIMARY)
        .add(Text("Контакты"), KeyboardButtonColor.PRIMARY).row()
        .add(Text("Доп.информация"), KeyboardButtonColor.PRIMARY).row()
        .add(Text("Оставить заявку"), KeyboardButtonColor.PRIMARY)
    )
    await msg.answer("🎮 Главное меню 🎮\n\n(Для повторного вызова меню в чате отправьте слово 'Меню')\n\n"
                     "Выберите нужную Вам опцию:", keyboard=keyboard)


async def links_keyboard(msg: Message):  # Клавиатура для торговых площадок
    keyboard = (
        Keyboard(inline=True)
        .add(OpenLink(platform_links.get("vk_market"), "Товары"))
        .add(OpenLink(platform_links.get("vk_service"), "Услуги")).row()
        .add(OpenLink(platform_links.get("far_post"), "Наш профиль на FarPost.ru"))
    )

    await msg.answer("📎 Ссылки 📎", keyboard=keyboard)


async def create_route_keyboard(msg: Message):  # Клавиатура для подтверждения перехода на маршрутные платформы
    keyboard = (
        Keyboard(inline=True)
        .add(Text("Да"), KeyboardButtonColor.POSITIVE)
        .add(Text("Нет"), KeyboardButtonColor.NEGATIVE)
    )

    await msg.answer("Уточнить наше местоположение на карте? 📍", keyboard=keyboard)


async def route_keyboard(msg: Message):  # Клавиатура для перехода на маршрутные платформы
    keyboard = (
        Keyboard(inline=True)
        .add(OpenLink(route_links.get("YANDEX"), "Яндекс Карты")).row()
        .add(OpenLink(route_links.get("2GIS"), "2ГИС")).row()
        .add(OpenLink(route_links.get("GOOGLE"), "Google Maps"))
    )

    await msg.answer("🗺 Наше местоположение\n\n"
                     "Выберите удобную для Вас платформу", keyboard=keyboard)


async def contacts_keyboard(msg: Message):  # Клавиатура с ссылками на аккаунты и контактным номером телефона
    keyboard = (
        Keyboard(inline=True)
        .add(OpenLink(contact_links.get("whatsapp"), "WhatsApp")).row()
        .add(OpenLink(contact_links.get("telegram"), "Telegram")).row()
        .add(OpenLink(contact_links.get("vk"), "VK"))
    )

    await msg.answer(f"📲 Наши контакты\n\nТелефон: {phone}", keyboard=keyboard)


async def answer_keyboard(msg: Message):  # Клавиатура для подтверждения корректности заявки клиента
    keyboard = (
        Keyboard(inline=True)
        .add(Text("Верно"), KeyboardButtonColor.POSITIVE)
        .add(Text("Неверно"), KeyboardButtonColor.NEGATIVE).row()
        .add(Text("Меню"), KeyboardButtonColor.PRIMARY)

    )
    await msg.answer("Все верно?", keyboard=keyboard)


async def check_of_correct(msg: Message):  # Клавиатура для перехода к проверке корректности заявки.
    keyboard = (                           # Является моим временным решением. Позже будет убрана
        Keyboard(inline=True)
        .add(Text("Проверить заявку"), KeyboardButtonColor.POSITIVE)
    )
    await msg.answer("Проверьте заявку на корректность", keyboard=keyboard)



