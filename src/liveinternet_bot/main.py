import matplotlib.pyplot as plt
import requests
import asyncio
import logging


from src.liveinternet_bot import config
from src.utils.CheckURL import CheckURL
from src.utils.plot import plot_traffic
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram import Router
from io import BytesIO
from aiogram.enums import ChatAction
from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart, Command

rt = Router()


# Обработчик команды /check_url
@rt.message(CommandStart())
async def start_check_url(message: types.Message, state: FSMContext):
    """ Обработчик команды /start
        Просит пользователя отправить сообщением URL,
        после чего встаёт в состояние ожидания сообщения.
    """
    await message.reply("Отправьте мне URL интересующего вас сайта")
    # Переходим в состояние ожидания URL
    await state.set_state(CheckURL.waiting_for_url)


# Обработчик ввода URL
@rt.message(StateFilter(CheckURL.waiting_for_url))
async def check_url_and_waiting_date(message: types.Message, state: FSMContext):
    """Обработчик состояния ожидания URL
       Получает URL от пользователя, выполняет запрос к API,
       проверяет наличие данных и запрашивает дату, если данные найдены.
    """
    # Получаем URL из сообщения пользователя
    domain = message.text

    # Базовый URL API
    base_url = "http://23.111.123.4:8000/data/"

    # Собираем полный URL для запроса
    full_url = base_url + domain

    # Выполняем запрос к API
    response = requests.get(full_url)

    # Проверяем статус кода ответа
    if response.status_code == 200:
        data = response.json()
        if 'error' in data:  # Если есть ошибка, данные отсутствуют
            await message.reply("Данные отсутствуют или URL введён некорректно")
        else:  # Если ошибки нет, данные существуют
            await message.reply("Пожалуйста, введите дату в формате YYYY-MM-DD или YYYY-MM-DD YYYY-MM-DD")
            # Сохраняем данные в состояние
            await state.update_data(data=data)
            # Переходим в состояние ожидания даты
            await state.set_state(CheckURL.waiting_for_date)


# Обработчик ввода даты
@rt.message(StateFilter(CheckURL.waiting_for_date))
async def process_date(message: types.Message, state: FSMContext):
    """ Обработчик состояния ожидания даты
        Получает дату от пользователя, проверяет наличие данных
        в указанный период и отправляет график трафика.
    """
    # Получаем дату из сообщения пользователя
    date_1 = message.text
    data_dict = await state.get_data()

    x = []
    y = []

    dates = date_1.split()

    if len(dates) == 1:
        # Введена одна дата
        date = dates[0]
        if date in data_dict:
            x.append(date)
            y.append(data_dict[date])
        else:
            await message.reply("Дата не найдена или введена некорректно")
            return
    elif len(dates) == 2:
        # Введены две даты
        start_date, end_date = dates
        for date, value in data_dict.items():
            if start_date <= date <= end_date:
                x.append(date)
                y.append(value)
        if not x:
            await message.reply("Даты не найдены или введены некорректно")
            return
    else:
        await message.reply("Введено слишком много дат")
        return

    await send_plot(message, x, y)

    # Сбрасываем состояние обработки даты
    await state.clear()


async def send_plot(message: types.Message, x, y):
    """Отправка графика трафика пользователю
       Создает график на основе переданных данных и отправляет его пользователю.
    """
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)

    # Создаем график и сохраняем его в буферный объект BytesIO
    buffer = BytesIO()
    local_plt = plt
    plot_traffic(x, y)
    local_plt.savefig(buffer, format='png')
    plt.clf()
    buffer.seek(0)  # Перемещаем указатель в начало буфера

    # Получаем байтовую строку из буферного объекта BytesIO
    image_bytes = buffer.getvalue()

    await message.reply_photo(photo=types.BufferedInputFile(file=image_bytes, filename="График"))


@rt.message(Command("help"))
async def handle_help(message: types.Message):
    """ Обработчик команды /help
        Отправляет сообщение с краткой информацией о боте.
    """
    await message.bot.send_message(message.from_user.id,
                                   'Бот "Historical liveinternet" предназначен для пострения графиков трафика '
                                   'новостных сайтов.\n'
                                   'Команда /start отвечает за начало работы бота.\n'
                                   'Вам будет необходимо знать URL сайта, график трафика которого вы хотите получить, '
                                   'а также конкретная дата или промежуток времени.')


async def main():
    logging.basicConfig(level=logging.INFO)
    dp = Dispatcher()
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp.include_router(rt)
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except asyncio.CancelledError:
        logging.info("Polling task was cancelled")


if __name__ == "__main__":
    asyncio.run(main())
