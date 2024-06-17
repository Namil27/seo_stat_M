import json


def take_old_tables(connection) -> list[str]:
    """
    Эта функция извлекает список всех таблиц в схеме 'public' базы данных PostgreSQL.

    :param connection: Объект, представляющий открытое соединение с базой данных.
    :return: Список имен таблиц в схеме 'public'.
    """
    try:
        cursor = connection.cursor()
        # Выполняем SQL-запрос для получения списка всех таблиц
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public'
        """)

        # Получаем результаты запроса
        tables = cursor.fetchall()
        tables_list = [table[0] for table in tables]
        cursor.close()
        connection.commit()
        return tables_list
    except Exception as error:
        print(f"Ошибка при подключении к базе данных: {error}")


def get_uniq_id_by_domain_name_sinx(connection, domain_name: str) -> str:
    """
    Синхронная функция для получения уникального идентификатора (uniq_id) по имени домена (domain_name).

    Эта функция выполняет запрос к таблице 'domain_mapping' для получения 'uniq_id',
    соответствующего переданному 'domain_name'.

    :param connection: Соединение с базой данных PostgreSQL.
    :param domain_name: Имя домена, для которого нужно получить уникальный идентификатор.
    :return: Уникальный идентификатор (uniq_id), соответствующий имени домена.
    :raises Exception: Если происходит ошибка при выполнении SQL команды или если 'domain_name' не найден.
    """
    query = '''
        SELECT uniq_id
        FROM domain_mapping
        WHERE domain_name = %s
    '''
    try:
        # Открываем курсор для выполнения запроса
        with connection.cursor() as cursor:
            # Выполнение запроса и получение результата
            cursor.execute(query, (domain_name,))
            result = cursor.fetchone()

            if result is None:
                raise Exception(f"Не найдено записи для domain_name: {domain_name}")

            return result[0]
    except Exception as e:
        print(f"Ошибка: {e}")
        raise


def save_data_as_json(connection, domain_name: str):
    """
    Эта функция извлекает все данные из указанной таблицы в базе данных PostgreSQL и сохраняет их в JSON файл.

    :param connection: Объект, представляющий открытое соединение с базой данных.
    :param domain_name: Название таблицы в базе данных и используемое для имени JSON файла.
    """
    with connection.cursor() as cursor:
        # Выполняем запрос для получения всех данных из таблицы
        cursor.execute(f'SELECT * FROM "{domain_name}";')
        rows = cursor.fetchall()
        data_dict = {}

        for row in rows:
            date = row[0].strftime('%Y-%m-%d')
            traffic = row[1]
            data_dict[date] = traffic

    # Сохраняем данные в JSON-файл
    with open(f"data/{domain_name}.json", "w") as data_json:
        json.dump(data_dict, data_json, indent=4)


def add_redaction_table(connection, uniq_id: str):
    """
    Эта функция создает таблицу для СМИ в базе данных liveinternet.

    :param connection: Объект, представляющий открытое соединение с базой данных.
    :param uniq_id: Уникальное обозначение на ли.ру.

    """

    cursor = connection.cursor()
    # Создаем таблицу для СМИ.
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS "{uniq_id}" (
        date DATE UNIQUE,
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

    # Сохраняем изменения и закрываем соединение
    connection.commit()


def insert_data_into_timescaledb_from_file(connection, uniq_id: str, domain: str):
    """
    Эта функция вставляет данные из JSON файла в таблицу TimescaleDB.

    :param connection: Объект, представляющий открытое соединение с базой данных.
    :param uniq_id: Уникальный идентификатор, используемый в качестве имени таблицы.
    :param domain: Доменное имя, используемое для формирования пути к JSON файлу.
    """
    json_file_path = f"data/{domain}.json"
    # Создание курсора для выполнения запросов
    cur = connection.cursor()

    # Загрузка данных из JSON файла
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Вставка данных в таблицу
    for date, traffic in data.items():
        cur.execute(f'INSERT INTO "{uniq_id}" (date, traffic) VALUES (%s, %s) ON CONFLICT (date) DO NOTHING',
                    (date, traffic))

    # Сохранение изменений в базе данных
    connection.commit()
    cur.close()


def delete_table(connection, table_name: str):
    """
    Эта функция удаляет указанную таблицу в базе данных PostgreSQL.

    :param connection: Объект, представляющий открытое соединение с базой данных.
    :param table_name: Название таблицы, которую необходимо удалить.
    """
    # Создание курсора для выполнения запросов
    cursor = connection.cursor()

    # Удаление таблиц
    cursor.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE')

    # Сохранение изменений в базе данных
    connection.commit()
    cursor.close()
