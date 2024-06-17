import os
import random
import time
import requests
import json
from PIL import Image
from io import BytesIO
from user_agents import USER_AGENTS


def add_redaction_table(uniq_id: str, connection):
    """
    Эта функция создает таблицу для СМИ в базе данных liveinternet.

    :param uniq_id: Название СМИ.
    :param connection: Объект, представляющий открытое соединение с базой данных.

    """

    cursor = connection.cursor()
    # Создаем таблицу для СМИ.
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS "{uniq_id}" (
        date DATE,
        traffic INTEGER
    );

    DO $$ BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = '{uniq_id}'
        ) THEN
            SELECT create_hypertable('{uniq_id}', 'date');
        END IF;
    END $$;
    """)

    connection.commit()


def add_data_in_table(name_redaction: str, today_date: str, traffic: int, connection):
    """
    Добавляет данные в табличку СМИ.

    :param name_redaction: Название СМИ.
    :param today_date: Сегодняшняя дата в формате yy-mm-dd.
    :param traffic: Трафик.
    :param connection: Объект, представляющий открытое соединение с базой данных.

    """

    cursor = connection.cursor()
    sql_insert_cmd = f"""INSERT INTO "{name_redaction}" VALUES (CURRENT_DATE, {traffic});"""

    cursor.execute(f"""SELECT * FROM "{name_redaction}" ORDER BY date DESC LIMIT 1;""")
    # print(name_redaction)
    result = cursor.fetchone()

    if result is not None:
        # Все преобразования ниже приводят данные в нужный вид, для сравнивания
        last_date = result[0].strftime('%Y-%m-%d')
        # Если запись не существует, выполнить запись данных
        if last_date != today_date:
            cursor.execute(sql_insert_cmd)
        else:
            pass
    else:
        cursor.execute(sql_insert_cmd)

    connection.commit()


def insert_missing_records(connection):
    """
    Функция для вставки отсутствующих записей в таблицы базы данных liveinternet.

    :param connection: Объект соединения psycopg2, соединение с базой данных PostgreSQL.

    Эта функция перебирает каждую таблицу в базе данных liveinternet и проверяет, существует ли запись для текущей даты.
    Если нет, она вставляет запись с текущей датой и значением трафика NULL.
    """

    cursor = connection.cursor()

    # Получаем список всех таблиц в базе данных liveinternet
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = cursor.fetchall()

    # Пробегаемся по каждой таблице
    for table in tables:
        table_name = table[0] if not table[0] == "domain_mapping" else None
        if table_name is None:
            continue

        # Проверяем, была ли сделана запись за сегодняшний день
        cursor.execute(f"""SELECT COUNT(*) FROM "{table_name}" WHERE date = CURRENT_DATE;""")
        count = cursor.fetchone()[0]

        # Если запись за сегодняшний день отсутствует, вставляем запись
        if count == 0:
            cursor.execute(f"""INSERT INTO "{table_name}" (date, traffic) VALUES (CURRENT_DATE, NULL);""")
            connection.commit()
            # print(f"""Вставлена запись в таблицу "{table_name}" за сегодня с traffic = None""")


def pars_reit_today(start_page: int, end_page: int) -> list[tuple[str, str, int]]:
    """
    Берет рейтинг с сайта www.liveinternet.ru сразу с нескольких страниц, и возвращает данные в виде списка.

    :param start_page: Стартовая страница, с которой начинается сбор рейтинга (от самых популярных).
    :param end_page: Конечная страница, на которой заканчивается сбор рейтинга (к менее популярным).
    :return today_reit: Список с картежами формата (название СМИ(строка), трафик(целое число))
    """
    # Список с возможным ненужным синтаксисом в названии редакций.
    literals = [
        '/', 'www.'
    ]
    delay = random.choice([0.1, 0.2])
    today_reit = []

    for i in range(start_page, end_page + 1):
        url_stat = f"https://www.liveinternet.ru/rating/ru/media/today.tsv?page={i}"
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        # Разбили строку на список, в каждом элементе которого хранятся данные о редакции в строковом виде.
        data_arr = requests.get(url_stat, headers=headers).text.split('\n')
        # Разбиваем каждую строку по символу "/", и вытаскиваем данные на 2 и 4 позиции(название и инфа соответственно).
        for edition in data_arr[1:-2]:
            data_list = repr(edition).split('\\')
            domain = data_list[1][1:]
            unique_id = data_list[0][1:]
            # Делаем имена редакций читабельными.
            for literal in literals:
                if literal in domain:
                    domain = domain.replace(literal, '')
            try:
                stat = int(data_list[3][1:])

            except Exception as e:
                print(f"Error: {e}")
                continue

            # Добавляем данные в список в виде кортежа.
            today_reit.append((unique_id, domain, stat))

            time.sleep(delay)
    return today_reit


def get_domain_name_by_uniq_id(connection, uniq_id: str) -> str:
    """
    Синхронная функция для получения имени домена (domain_name) по уникальному идентификатору (uniq_id).

    :param connection: Соединение с базой данных PostgreSQL.
    :param uniq_id: Уникальный идентификатор, для которого нужно получить имя домена.
    :return: Имя домена (domain_name), соответствующее переданному уникальному идентификатору.
    :raises Exception: Если происходит ошибка при выполнении SQL команды или если 'uniq_id' не найден.
    """
    query = '''
        SELECT domain_name
        FROM domain_mapping
        WHERE uniq_id = %s
    '''
    try:
        cursor = connection.cursor()
        cursor.execute(query, (uniq_id,))
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            raise Exception(f"Не найдено записи для uniq_id: {uniq_id}")
        return result[0]
    except Exception as e:
        print(f"Error: {e}")
        raise


def get_last_data_medias_json(connection):
    """
    Функция для извлечения последних записей из таблиц базы данных liveinternet и сохранения в файл JSON.

    :param connection: Объект соединения psycopg2, соединение с базой данных PostgreSQL.
    :return: None

    Эта функция выполняет SQL-запросы для каждой таблицы в базе данных "liveinternet" с целью получения последней
    записи. Полученные данные затем сортируются по убыванию значений трафика и сохраняются в файл JSON
    под названием "rating.json". Если происходит ошибка при подключении к базе данных или выполнении SQL-запроса,
    ошибка будет выведена в консоль.

    """

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            rows = cursor.fetchall()
            last_records = {}
            for row in rows:
                uniq_id = row[0] if not row[0] == "domain_mapping" else None
                if uniq_id is None:
                    continue
                media = get_domain_name_by_uniq_id(connection, uniq_id)
                cursor.execute(f"""SELECT traffic FROM "{uniq_id}" ORDER BY date DESC LIMIT 1""")
                last_traffic = cursor.fetchone()[0]
                last_records[media] = last_traffic
            # Сортировка словаря по убыванию ключей
            sorted_records = dict(
                sorted(last_records.items(), key=lambda x: x[1] if x[1] is not None else float('-inf'), reverse=True)
            )
            # Сохранение словаря в файл JSON
            with open("/app/data/rating.json", "w") as json_file:
                json.dump(sorted_records, json_file, ensure_ascii=False, indent=4)
            # Закрываем соединение.
            connection.close()

    except Exception as e:
        print(f"Error: {e}")


def parsing_ico(media: str):
    """
       Функция для загрузки и сохранения иконки с веб-сайта liveinternet.ru.

       Эта функция принимает имя медиа (media), формирует URL для загрузки иконки в формате ICO,
       проверяет, существует ли иконка в локальной директории, и, если не существует, загружает ее,
       сохраняет в указанную директорию и делает задержку на случайное время от 0.1 до 0.5 секунд.

       :param media: Имя медиа, используемое для формирования URL и имени файла иконки.
       """
    # URL иконки
    url = f"https://www.liveinternet.ru/favicon/{media}.ico"
    icon_name = f"{media}.ico"
    delay = random.choice([0.1, 0.2])
    # Директория для сохранения иконок
    icon_dir = 'icons'
    icon_path = icon_dir + '/' + icon_name

    if not os.path.exists(icon_path):
        try:
            # Загрузка ICO файла с веб-сайта
            response = requests.get(url, headers={'User-Agent': random.choice(USER_AGENTS)})
            # Открытие изображения с помощью Pillow
            icon = Image.open(BytesIO(response.content))
            # Сохранение иконки
            icon.save(icon_path)
            time.sleep(delay)
        except Exception as e:
            print(f"Error: {e}")
    else:
        pass


def domain_mapper(connection, domain_name: str, uniq_id: str):
    """
       Функция для вставки или обновления сопоставления домена в базе данных.

       Эта функция создает таблицу с именем 'domain_mapping', если она еще не существует,
       с колонками 'uniq_id' (TEXT, первичный ключ, NOT NULL) и 'domain_name' (TEXT, NOT NULL).
       Затем она вставляет новую запись с 'uniq_id' и 'domain_name'. Если строка с таким же
       'uniq_id' уже существует, то функция обновляет 'domain_name' для этого 'uniq_id'.

       :param connection: Объект подключения psycopg2 к базе данных PostgreSQL.
       :param domain_name: Имя домена, которое нужно вставить или обновить.
       :param uniq_id: Уникальный идентификатор, связанный с именем домена.

       :raises Exception: Если происходит ошибка при выполнении SQL команд.
    """
    add_mapping_table = '''
        CREATE TABLE IF NOT EXISTS domain_mapping (
            uniq_id TEXT PRIMARY KEY NOT NULL,
            domain_name TEXT NOT NULL
        )
    '''
    insert_sql_com = '''
        INSERT INTO domain_mapping (uniq_id, domain_name)
        VALUES (%s, %s)
        ON CONFLICT (uniq_id) DO UPDATE SET domain_name = EXCLUDED.domain_name
    '''

    try:
        cursor = connection.cursor()
        # Создание таблицы, если она еще не создана
        cursor.execute(add_mapping_table)
        cursor.execute(insert_sql_com, (uniq_id, domain_name))
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")
