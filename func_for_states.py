# .py файл для создания клавиатур и переменных под Стейты (Отправка заявки)

from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text

about_size = "📄 Оформление заявки\n\nВведите характеристики шины в такой последовательности:\n\n"\
             "1⃣ Ширина профиля\n2⃣ Высота профиля\n3⃣ Посадочный диаметр\n\n"\
             "Пример сообщения:\n'225/45/ R17'"

about_brand = "©️ Введите марку шины\n(по желанию)\n\n"\
              "Пример:\n'Bridgestone' или 'BFGoodrich'\n\n"\
              "Если нет определенного ответа, то напишите '-'"

about_quantity = "Введите количество шин (по желанию)\n\n" \
                 "Пример: '2' или '4'\n\n" \
                 "Если нет определенного ответа, то отправьте '-'"

about_contact = "Пожалуйста, оставьте Ваш контактный номер, чтобы мы смогли связаться с Вами:"


async def bus_condition(msg: Message):  # Клавиатура для отправки состояния шин
    keyboard = (
        Keyboard(inline=True)
        .add(Text("Новое"), KeyboardButtonColor.PRIMARY)
        .add(Text("Б/У"), KeyboardButtonColor.PRIMARY)
    )
    await msg.answer(f"♻ Выберите желаемое состояние товара: ", keyboard=keyboard)


async def tire_season(msg: Message):  # Клавиатура для отправки сезона шин
    keyboard = (
        Keyboard(inline=True)
        .add(Text("Летняя"), KeyboardButtonColor.PRIMARY)
        .add(Text("Зимняя"), KeyboardButtonColor.PRIMARY).row()
        .add(Text("Грязь АТ"), KeyboardButtonColor.PRIMARY)
        .add(Text("Грязь МТ"), KeyboardButtonColor.PRIMARY)
    )
    await msg.answer("📆 Выберите желаемый протектор (сезон)", keyboard=keyboard)


async def tire_studding(msg: Message):  # Клавиатура для отправки шиповки шин
    keyboard = (
        Keyboard(inline=True)
        .add(Text("Шипы"), KeyboardButtonColor.PRIMARY)
        .add(Text("Без шипов"), KeyboardButtonColor.PRIMARY)
    )
    await msg.answer("⚙ Выберите желаемый параметр шиповки", keyboard=keyboard)


async def tire_type(msg: Message):  # Клавиатура для отправки типа шин
    keyboard = (
        Keyboard(inline=True)
        .add(Text("Обычная"), KeyboardButtonColor.PRIMARY)
        .add(Text("Грузовая и LT"), KeyboardButtonColor.PRIMARY)
    )
    await msg.answer("🚜 Выберите тип шины", keyboard=keyboard)


async def checker(msg: Message):  # Проверяет, верно ли пользователь оставил заявку
    if msg.text == "Верно":
        menu = (
            Keyboard(inline=True)
            .add(Text("Меню"), KeyboardButtonColor.PRIMARY)
        )
        await msg.answer("✅ Отлично. Ваша заявка обработана. Через некоторое время мы Вам перезвоним!\n\n"
                         "Нажмите 'Меню', чтобы вернуться в главное меню", keyboard=menu)
    elif msg.text == "Не верно":
        keyboard = (
            Keyboard(inline=True)
            .add(Text("Переоформить заявку"), KeyboardButtonColor.POSITIVE)
        )
        await msg.answer("Пожалуйста, заполните заявку заново", keyboard=keyboard)
