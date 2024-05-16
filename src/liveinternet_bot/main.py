import matplotlib.pyplot as plt
import tempfile
import requests
import config
import asyncio
import logging

from io import BytesIO
from aiogram.enums import ChatAction
from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart, Command


dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.bot.send_message(message.from_user.id, 'Введите команду /plot для начала работы')


@dp.message(Command("help"))
async def handle_help(message: types.Message):
    await message.bot.send_message(message.from_user.id, 'Бот предназначен для построение графика трафика выбранного сайта за определённую дату или промежуток времени. Команда /plot отвечает за построение графика ')


@dp.message(Command('plot'))
async def send_plot(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    )

    def plot_traffic(x, y):
        # Проверяем количество данных
        if len(x) > 1 and len(y) > 1:
            # Если есть достаточно данных, строим линейный график
            plt.plot(x, y)
        elif len(x) == 1 and len(y) == 1:
            # Если данных меньше двух значений, строим точечный график
            plt.scatter(x, y)
        else:
            print("Недостаточно данных для построения графика")

        # Настройка осей и отображение графика
        plt.xlabel("Дата")
        plt.ylabel("Трафик")
        plt.title("График трафика")

    # Пример данных
    x = [1, 6, 89, 234, 555]  # Дата
    y = [10000, 13456, 1948, 4567, 23456]  # Трафик

    # Создаем график и сохраняем его в буферный объект BytesIO
    buffer = BytesIO()
    local_plt = plt
    plot_traffic(x, y)
    local_plt.savefig(buffer, format='png')
    buffer.seek(0)  # Перемещаем указатель в начало буфера

    # Получаем байтовую строку из буферного объекта BytesIO
    image_bytes = buffer.getvalue()

    await message.reply_photo(
        photo=types.BufferedInputFile(
            file=image_bytes,
            filename="График",
        )
    )


'''# Базовый URL API
base_url = "http://23.111.123.4:8000/data/"

# Обработчик команды /check_url
@dp.message(Command('check_url'))
async def check_url(message: types.Message):
    # Получаем домен от пользователя
    domain = message.text.split(maxsplit=1)[1]

    # Собираем полный URL для запроса
    full_url = base_url + domain

    # Выполняем запрос к API
    response = requests.get(full_url)

    # Проверяем статус кода ответа
    if response.status_code == 200:
        await message.reply("URL обнаружен")
    else:
        await message.reply("Ошибка URL")'''


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
