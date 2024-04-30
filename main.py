import psycopg2

from fastapi import FastAPI
from src.conn_info.con_info import connect_args_user


def get_data_as_json(media: str):
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
def get_data(media: str):
    try:
        data = get_data_as_json(media)
        return data
    except Exception as e:
        return {"error": str(e)}
