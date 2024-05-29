import pytest

from io import BytesIO
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.enums import ChatAction
from aiogram.types import Message, Chat, User, BufferedInputFile
from aiogram.fsm.context import FSMContext
from unittest.mock import AsyncMock, patch, MagicMock
from src.liveinternet_bot import config
from src.utils.CheckURL import CheckURL
from src.liveinternet_bot.main import start_check_url, check_url_and_waiting_date, send_plot
from aioresponses import aioresponses


@pytest.fixture
def bot():
    """
    Фикстура для создания мока бота.

    Создает и возвращает мок бота с указанным токеном.
    """
    return Bot(token=config.BOT_TOKEN)


@pytest.fixture
def dispatcher():
    """
    Фикстура для создания диспетчера.

    Создает и возвращает мок диспетчера.
    """
    return Dispatcher()


@pytest.fixture
def state():
    """
    Фикстура для создания мока состояния.

    Создает и возвращает мок состояния.
    """
    return AsyncMock(spec=FSMContext)


@pytest.fixture
def message():
    """
    Фикстура для создания мока сообщения.

    Создает и возвращает мок сообщения с заполненными полями.
    """
    msg = MagicMock(spec=Message)
    msg.bot = MagicMock(spec=Bot)
    msg.bot.send_chat_action = AsyncMock()
    msg.chat = MagicMock(spec=Chat)
    msg.chat.id = 123456
    msg.from_user = MagicMock(spec=User)
    msg.from_user.id = 654321
    msg.reply_photo = AsyncMock()
    msg.reply = AsyncMock()
    return msg


# Тест для команды /start
@pytest.mark.asyncio
async def test_start_check_url(message, state):
    """
    Тест для команды /start.

    Проверяет, что при вызове команды /start пользователю возвращается
    сообщение "Отправьте мне URL интересующего вас сайта" и устанавливается
    соответствующее состояние FSMContext.
    """
    message.text = "/start"
    message.reply = AsyncMock()

    await start_check_url(message, state)

    message.reply.assert_called_with("Отправьте мне URL интересующего вас сайта")
    state.set_state.assert_called_with(CheckURL.waiting_for_url)


# Тест для обработки URL
@pytest.mark.asyncio
async def test_check_url_and_waiting_date(message, state):
    """
    Тест для обработки URL и ожидания даты.

    Проверяет, что функция check_url_and_waiting_date корректно обрабатывает URL,
    выполняет запрос к API и ожидает дату, если данные найдены. В случае отсутствия данных
    или некорректного ввода URL должно возвращаться соответствующее сообщение.

    Подставляет в мокированный запрос данные ошибка для тестирования сценария,
    когда данные отсутствуют или URL введён некорректно.

    Проверяет, что возвращается ожидаемое сообщение пользователю.

    """
    message.text = "example.com"
    mock_response_data = {
        "error": "Some error message"}  # Подставьте сюда сообщение об ошибке, которое возвращает ваш API

    # Мокируем запрос и возвращаемый ответ
    with aioresponses() as mocked_responses:
        mocked_responses.get("http://23.111.123.4:8000/data/example.com", payload=mock_response_data)

        # Вызываем функцию для тестирования
        await check_url_and_waiting_date(message, state)

    # Проверяем вызовы и ожидаемые результаты
    message.reply.assert_called_with("Данные отсутствуют или URL введён некорректно")  # Изменили текст сообщения


# Тест для отправки графика
@pytest.mark.asyncio
@patch('src.Liveinternet_bot.main.plt')
async def test_send_plot(mock_plt, message, bot):
    x = ["2023-01-01", "2023-01-02"]
    y = [100, 200]

    buffer = BytesIO()
    mock_plt.savefig.return_value = buffer

    await send_plot(message, x, y)

    message.bot.send_chat_action.assert_called_with(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
    message.reply_photo.assert_called_once()
    args, kwargs = message.reply_photo.call_args
    assert isinstance(kwargs['photo'], BufferedInputFile)
