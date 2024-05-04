import json
import psycopg2

from fastapi import FastAPI
from src.conn_info.con_info import connect_args_user


def get_data_as_json(media: str):
    """
    Функция для извлечения данных из таблицы базы данных и возврата в формате JSON.

    :param media: Название таблицы базы данных, из которой нужно извлечь данные.

    return data: Словарь, содержащий данные из таблицы. Ключи - это даты в формате '%Y-%m-%d', а
                 значения - соответствующие значения трафика.

    Если происходит ошибка при подключении к базе данных или выполнении SQL-запроса, функция выводит
    сообщение об ошибке и возвращает None.
    """
    try:
        with psycopg2.connect(**connect_args_user) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""SELECT * FROM "{media}";""")
            rows = cursor.fetchall()
            data = {row[0].strftime('%Y-%m-%d'): row[1] for row in rows}
            return data
    except Exception as e:
        print(f"Error: {e}")


app = FastAPI()


@app.get("/data/{media}")
# Функция меода GET, которая возвращает json  сданными по конкретному адрессу.
def get_data(media: str):
    try:
        data = get_data_as_json(media)
        return data
    except Exception as e:
        return {"error": str(e)}


@app.get("/medias")
def get_list_medias():
    try:
        with open('src/parser/rating.json') as file:
            rating = json.load(file)
        return rating
    except Exception as e:
        return {"error": str(e)}
