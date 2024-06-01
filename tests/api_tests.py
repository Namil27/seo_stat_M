import json
import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock, MagicMock

# Предположим, что app - это ваш FastAPI экземпляр, который импортирован из основного модуля приложения.
from src.liveinternet.api.main import app

# Тестовые данные
sample_data = {
    "media1": 5,
    "media2": 4.5,
    "media3": 4
}
sample_data_json = json.dumps(sample_data)


@pytest.mark.asyncio
async def test_get_list_medias_success():
    """
    Тест успешного получения списка медиа.

    Этот тест проверяет, что при успешном открытии файла с данными медиа,
    возвращается правильный список медиа и статус ответа 200.
    """
    # Создаем мок для асинхронного контекстного менеджера
    mock_file = MagicMock()
    mock_file.__aenter__ = AsyncMock(return_value=mock_file)
    mock_file.__aexit__ = AsyncMock(return_value=None)
    mock_file.read = AsyncMock(return_value=sample_data_json)

    # Мокаем открытие файла и чтение данных
    with patch("aiofiles.open", return_value=mock_file):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/medias")
            assert response.status_code == 200
            assert response.json() == sample_data


@pytest.mark.asyncio
async def test_get_list_medias_error():
    """
    Тест ошибки при получении списка медиа.

    Этот тест проверяет, что при ошибке открытия файла с данными медиа,
    возвращается сообщение об ошибке и статус ответа 200.
    """
    # Создаем мок для асинхронного контекстного менеджера с ошибкой
    mock_file = MagicMock()
    mock_file.__aenter__ = AsyncMock(side_effect=Exception("File not found"))

    # Мокаем открытие файла и чтение данных
    with patch("aiofiles.open", return_value=mock_file):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/medias")
            assert response.status_code == 200
            assert response.json() == {"error": "File not found"}
