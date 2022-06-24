# .py файл для создания клавиатур для Стейтов (Отправка заявки)

from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text


async def bus_condition_keyboard(msg: Message):  # Клавиатура для отправки состояния шин
    keyboard = (
        Keyboard(inline=True)
        .add(Text("Новое"), KeyboardButtonColor.PRIMARY)
        .add(Text("Б/У"), KeyboardButtonColor.PRIMARY)
    )
    await msg.answer(f"♻ Выберите желаемое состояние товара: ", keyboard=keyboard)


async def tire_season_keyboard(msg: Message):  # Клавиатура для отправки сезона шин
    keyboard = (
        Keyboard(inline=True)
        .add(Text("Летняя"), KeyboardButtonColor.PRIMARY)
        .add(Text("Зимняя"), KeyboardButtonColor.PRIMARY).row()
        .add(Text("Грязь АТ"), KeyboardButtonColor.PRIMARY)
        .add(Text("Грязь МТ"), KeyboardButtonColor.PRIMARY)
    )
    await msg.answer("📆 Выберите желаемый протектор (сезон)", keyboard=keyboard)


async def tire_studding_keyboard(msg: Message):  # Клавиатура для отправки шиповки шин
    keyboard = (
        Keyboard(inline=True)
        .add(Text("Шипы"), KeyboardButtonColor.PRIMARY)
        .add(Text("Без шипов"), KeyboardButtonColor.PRIMARY)
    )
    await msg.answer("⚙ Выберите желаемый параметр шиповки", keyboard=keyboard)


async def tire_type_keyboard(msg: Message):  # Клавиатура для отправки типа шин
    keyboard = (
        Keyboard(inline=True)
        .add(Text("Обычная"), KeyboardButtonColor.PRIMARY)
        .add(Text("Грузовая и LT"), KeyboardButtonColor.PRIMARY)
    )
    await msg.answer("🚜 Выберите тип шины", keyboard=keyboard)

