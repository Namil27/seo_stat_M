import psycopg2

from datetime import datetime
from parsing_functions import *


def full_cycle():
    """
    Функция собирающая данные и записывающая их в БД.
    """
    # Подключаемся к базе данных
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME")
    )
    # Сохраняем данные в today_media_reit.
    today_media_reit = pars_reit_today(1, 50)
    current_date = datetime.now().strftime('%Y-%m-%d')
    # Пробегаемся по каждому сми и записываем данные в соответствующую табличку в БД и парсим иконки.
    for media in today_media_reit:
        add_redaction_table(media[0], connection)
        add_data_in_table(media[0], current_date, media[1], connection)
        parsing_ico(media[0])
    # Закрываем конект.
    connection.close()


def main():
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
        finally:
            # Если во второй раз по какой-то причине что-то не спарсил,то пробегаемся по всем табличкам и вставляем None
            # во все которые сегодня не вошли в топ 120.
            insert_missing_records(connection=psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                dbname=os.getenv("DB_NAME")
            ))
            # Сохраняем рейтинг для фронта.
            get_list_medias_as_json(connection=psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                dbname=os.getenv("DB_NAME")
            ))


if __name__ == "__main__":
    main()
