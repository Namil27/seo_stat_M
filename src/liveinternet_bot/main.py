import matplotlib.pyplot as plt
import requests
import config
import asyncio
import logging

from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import State, StatesGroup
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


class CheckURL(StatesGroup):
    waiting_for_url = State()
    waiting_for_date = State()


def plot_traffic(x, y):
    # Проверяем количество данных
    if len(x) > 1 and len(y) > 1:
        # Если есть достаточно данных, строим линейный график
        plt.plot(x, y)
    elif len(x) == 1 and len(y) == 1:
        # Если данных меньше двух значений, строим точечный график
        plt.scatter(x, y)

    # Настройка осей и отображение графика
    plt.xlabel("Дата")
    plt.ylabel("Трафик")
    plt.title("График трафика")


# Обработчик команды /check_url
@rt.message(CommandStart())
async def start_check_url(message: types.Message, state: FSMContext):
    await message.reply("Отправьте мне URL интересующего вас сайта")
    # Переходим в состояние ожидания URL
    await state.set_state(CheckURL.waiting_for_url)


# Обработчик ввода URL
@rt.message(StateFilter(CheckURL.waiting_for_url))
async def check_url(message: types.Message, state: FSMContext):
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
        '''else:
            await message.reply("Даты не найдены или введены некорректно")
            return'''
    else:
        await message.reply("Введено слишком много дат")
        return

    await send_plot(message, x, y)

    # Сбрасываем состояние обработки даты
    await state.clear()


async def send_plot(message: types.Message, x, y):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)

    # Создаем график и сохраняем его в буферный объект BytesIO
    buffer = BytesIO()
    local_plt = plt
    plot_traffic(x, y)
    local_plt.savefig(buffer, format='png')
    buffer.seek(0)  # Перемещаем указатель в начало буфера

    # Получаем байтовую строку из буферного объекта BytesIO
    image_bytes = buffer.getvalue()

    await message.reply_photo(photo=types.BufferedInputFile(file=image_bytes, filename="График"))


@rt.message(Command("help"))
async def handle_help(message: types.Message):
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
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit) as e:
        print(e)
