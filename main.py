import aiofiles
import asyncpg
import json
from fastapi import FastAPI, HTTPException

from src.conn_info.con_info import connect_args_user


async def get_data_as_json(media: str):
    """
    Асинхронная функция для извлечения данных из таблицы базы данных и возврата в формате JSON.

    :param media: Название таблицы базы данных, из которой нужно извлечь данные.
    :type media: str

    :return: Словарь, содержащий данные из таблицы. Ключи - это даты в формате '%Y-%m-%d', а значения -
    соответствующие значения трафика.
    :rtype: dict

    Если происходит ошибка при подключении к базе данных или выполнении SQL-запроса, функция поднимает исключение
    HTTPException с соответствующим статусом ошибки.
    """
    conn = None
    try:
        conn = await asyncpg.connect(**connect_args_user)
        async with conn.transaction():
            rows = await conn.fetch(f"""SELECT * FROM "{media}";""")
            data = {row[0].strftime('%Y-%m-%d'): row[1] for row in rows}
            return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            await conn.close()

app = FastAPI()


@app.get("/data/{media}")
async def get_data(media: str):
    """
    Асинхронный метод GET, который возвращает JSON с данными по конкретному адресу.

    :param media: Название таблицы базы данных, для которой нужно получить данные.
    :type media: str

    :return: Словарь с данными из таблицы.
    :rtype: dict

    Если происходит ошибка, функция возвращает словарь с ключом "error" и описанием ошибки.
    """
    try:
        data = await get_data_as_json(media)
        return data
    except Exception as e:
        return {"error": str(e)}


@app.get("/medias")
async def get_list_medias():
    """
    Асинхронный метод GET, который возвращает список медиа с их рейтингом.

    :return: Словарь, содержащий медиа и их рейтинг.
    :rtype: dict

    Если происходит ошибка, функция возвращает словарь с ключом "error" и описанием ошибки.
    """
    try:
        async with aiofiles.open('src/parser/rating.json', mode='r') as file:
            rating = await file.read()
        return json.loads(rating)
    except Exception as e:
        return {"error": str(e)}
