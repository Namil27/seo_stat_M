import psycopg2

from datetime import datetime
from parsing_functions import *
from src.conn_info.con_info import connect_args_parser


def full_cycle():
    """
    Функция собирающая данные и записывающая их в БД.
    """
    # Подключаемся к базе данных
    connection = psycopg2.connect(**connect_args_parser)
    # Сохраняем данные в today_media_reit.
    today_media_reit = pars_reit_today(1, 4)
    current_date = datetime.now().strftime('%Y-%m-%d')
    # Пробегаемся по каждому сми и записываем данные в соответствующую табличку в БД.
    for media in today_media_reit:
        add_redaction_table(media[0], connection)
        add_data_in_table(media[0], current_date, media[1], connection)
    # Закрываем конект.
    connection.close()


# Выполняем код.
try:
    full_cycle()

except Exception as e:
    print('Error: ', e)

finally:
    # Повторно парсим, если в первый раз по какой-то причине что-то не с парсилось.
    try:
        full_cycle()
    except Exception as e:
        print('Error: ', e)
    # Если и во второй раз по какой-то причине что-то не спарсилось, то пробегвемся по всем табличкам и вставлем None
    # во все котоые сегодня не вошли в топ 120.
    finally:
        insert_missing_records(connection=psycopg2.connect(**connect_args_parser))
