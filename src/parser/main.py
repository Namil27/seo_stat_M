from datetime import datetime

import psycopg2

from DataBase_connection import *
from full_cycle_funcs import *


def full_cycle():
    """
    Функция собирающая данные и записывающая их в БД.
    """
    # Подключаемся к базе данных
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    # Сохраняем данные в today_media_reit.
    today_media_reit = pars_reit_today(1, 4)
    current_date = datetime.now().strftime('%Y-%m-%d')

    for media in today_media_reit:
        add_redaction_table(media[0], connection)
        add_data_in_table(media[0], current_date, media[1], connection)

    # Пробегвемся по всем табличкам и вставлем None во все котоые сегодня не вошли.
    insert_missing_records(connection)

    connection.close()


# Выполнем код.
full_cycle()
