import asyncpg
import asyncio
from fastapi import FastAPI
from src.conn_info.con_info import connect_args_user

app = FastAPI()


class ConnectionPool:
    def __init__(self, min_size=10, max_size=100, **connect_args):
        self.min_size = min_size
        self.max_size = max_size
        self.connect_args = connect_args
        self._pool = []

    async def init_pool(self):
        for _ in range(self.min_size):
            conn = await asyncpg.connect(**self.connect_args)
            self._pool.append(conn)

    async def acquire(self):
        if not self._pool:
            if len(self._pool) < self.max_size:
                conn = await asyncpg.connect(**self.connect_args)
                return conn
            else:
                raise Exception("Connection pool is full")
        else:
            return self._pool.pop()

    async def release(self, conn):
        self._pool.append(conn)


async def get_data_as_json(media: str):
    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM table")
            data = [{"column1": row[0], "column2": row[1]} for row in rows]
            return data
    except asyncpg.exceptions.PostgresError as e:
        print("Ошибка при работе с PostgreSQL:", e)
        return None

# Создаем пул соединений
pool = ConnectionPool(min_size=5, max_size=10, **connect_args_user)

# Инициализируем пул соединений
asyncio.run(pool.init_pool())


# Маршрут для получения данных в формате JSON
@app.get("/data/{media}")
async def get_data(media: str):
    if media not in media_list:
        return {"error": "СМИ с таким названием не найдено"}
    else:
        # Здесь вы можете использовать функцию get_data_as_json для получения данных для конкретного СМИ
        # и возвращать их
        data = await get_data_as_json(media)
        return data
