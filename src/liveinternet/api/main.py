import aiofiles
import asyncpg
import json
import os
from fastapi import FastAPI, HTTPException


async def get_uniq_id_by_domain_name(connection, domain_name: str) -> str:
    """
    Асинхронная функция для получения уникального идентификатора (uniq_id) по имени домена (domain_name).

    Эта функция выполняет запрос к таблице 'domain_mapping' для получения 'uniq_id',
    соответствующего переданному 'domain_name'.

    :param connection: Асинхронное соединение с базой данных PostgreSQL.
    :param domain_name: Имя домена, для которого нужно получить уникальный идентификатор.
    :return: Уникальный идентификатор (uniq_id), соответствующий имени домена.
    :raises Exception: Если происходит ошибка при выполнении SQL команды или если 'domain_name' не найден.
    """
    query = '''
        SELECT uniq_id
        FROM domain_mapping
        WHERE domain_name = $1
    '''
    try:
        # Выполнение запроса и получение результата
        result = await connection.fetchval(query, domain_name)
        if result is None:
            raise Exception(f"Не найдено записи для domain_name: {domain_name}")
        return result
    except Exception as e:
        print(f"Ошибка: {e}")
        raise


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
        conn = await asyncpg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        uniq_id = await get_uniq_id_by_domain_name(conn, media)
        async with conn.transaction():
            rows = await conn.fetch(f"""SELECT * FROM "{uniq_id}";""")
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
        async with aiofiles.open('data/rating.json', mode='r') as file:
            rating = await file.read()
        return json.loads(rating)
    except Exception as e:
        return {"error": str(e)}
