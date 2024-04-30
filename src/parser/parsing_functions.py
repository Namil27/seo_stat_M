import requests


def add_redaction_table(red_name: str, connection):
    """
    Эта функция создает таблицу для СМИ в в базе данных liveinternet.

    :param red_name: Название СМИ.
    :param connection: Объект, представляющий открытое соединение с базой данных.

    """

    cursor = connection.cursor()
    # Создаем таблицу для СМИ.
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS "{red_name}" (
        date DATE,
        traffic INTEGER
    );

    DO $$ BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = '{red_name}'
        ) THEN
            SELECT create_hypertable('{red_name}', 'date');
        END IF;
    END $$;
    """)

    # Сохраняем изменения и закрываем соединение
    connection.commit()


def add_data_in_table(name_redacton: str, today_date: str, traffic: int, connection):
    """
    Добавляет данные в табличку СМИ.

    :param name_redacton: Название СМИ.
    :param today_date: Сегодняшняя дата в формате yy-mm-dd.
    :param traffic: Траффик.
    :param connection: Объект, представляющий открытое соединение с базой данных.

    """

    cursor = connection.cursor()
    sql_insert_cmd = f"""INSERT INTO "{name_redacton}" VALUES (CURRENT_DATE, {traffic});"""

    cursor.execute(f"""SELECT * FROM "{name_redacton}" ORDER BY date DESC LIMIT 1;""")
    # print(name_redacton)
    result = cursor.fetchone()

    if result is not None:
        last_date_obj = result[0]
        last_date_year = str(last_date_obj.year)
        last_date_month = str(last_date_obj.month) if last_date_obj.month // 10 != 0 else '0' + str(last_date_obj.month)
        last_date_day = str(last_date_obj.day) if last_date_obj.day // 10 != 0 else '0' + str(last_date_obj.day)
        last_date = last_date_year + '-' + last_date_month + '-' + last_date_day
        # Если запись не существует, выполнить запись данных
        if last_date != today_date:
            cursor.execute(sql_insert_cmd)
        else:
            pass
    else:
        cursor.execute(sql_insert_cmd)

    connection.commit()


def insert_missing_records(connection):
    cursor = connection.cursor()

    # Получить список всех таблиц в базе данных liveinternet
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = cursor.fetchall()

    # Пробегаемся по каждой таблице
    for table in tables:
        table_name = table[0]

        # Проверяем, была ли сделана запись за сегодняшний день
        cursor.execute(f"""SELECT COUNT(*) FROM "{table_name}" WHERE date = CURRENT_DATE;""")
        count = cursor.fetchone()[0]

        # Если запись за сегодняшний день отсутствует, вставляем запись
        if count == 0:
            cursor.execute(f"""INSERT INTO "{table_name}" (date, traffic) VALUES (CURRENT_DATE, NULL);""")
            connection.commit()
            # print(f"""Вставлена запись в таблицу "{table_name}" за {current_date} с traffic = None""")

    connection.close()


def pars_reit_today(start_page: int, end_page: int) -> list[tuple[str, int]]:
    """
    Берет рейтинг с сайта www.liveinternet.ru сразу с нескольких страниц, и возвращает данные в виде списука.

    :param start_page: Стартовая страница, с которой начинаеться сбор рейтинга (от самых популярных).
    :param end_page: Конечная страница, на которой заканчиваеться сбор рейтинга (к менее популярным).
    :return today_reit: Список с картежами формата (название СМИ(строка), трафик(цулое число))
    """
    # Список с возможным ненужным синтаксисом в названии редакций.
    litterals = [
        '/', 'www.'
    ]
    today_reit = []

    for i in range(start_page, end_page+1):
        url_stat = f"https://www.liveinternet.ru/rating/ru/media/today.tsv?page={i}"
        # Разбили строку на спиок, в каждом элементе которого храняться данные о редакции в строков виде.
        data_arr = requests.get(url_stat).text.split('\n')
        # Разбиваем каждую строку по символу "/", и вытаскиваем данные на 3 и 4 позиции(название и инфа соответственно).
        for edition in data_arr[1:-2]:
            name = repr(edition).split('\\')[1][1:]
            stat = int(repr(edition).split('\\')[3][1:])
            # Делаем имена редакций читабельными.
            for litteral in litterals:
                if litteral in name:
                    name = name.replace(litteral, '')
            # Добавляем данные в список в виде кортежа.
            today_reit.append((name, stat))

    return today_reit
