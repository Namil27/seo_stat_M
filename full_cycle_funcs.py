import sqlite3
import requests


def add_redaction_table(red_name: str):
    """
    Эта функция создает таблицу для СМИ в файле "reit_database.db".

    :param red_name: Название СМИ.(строка)
    """
    connection = sqlite3.connect('DATABASE/reit_data.db')
    cursor = connection.cursor()
    # Создаем таблицу для СМИ.
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS [{red_name}] (
       date TEXT,
       traffic INTEGER);
       ''')
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()


def add_data_in_table(name_redacton: str, date: str, traffic: int):
    """
    Добавляет данные в табличку СМИ.

    :param name_redacton: Название СМИ.
    :param date: Дата в виде DD-MM-YYYY.
    :param traffic: Целое число трафика.
    """
    connection = sqlite3.connect('DATABASE/reit_data.db')
    cursor = connection.cursor()

    cursor.execute(f"INSERT INTO [{name_redacton}] (date, traffic) VALUES (?, ?)", (f"{date}", traffic))

    connection.commit()
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
        '&quot;', '&lt;', '&gt'
    ]
    today_reit = []

    for i in range(start_page, end_page+1):
        url_stat = f"https://www.liveinternet.ru/rating/ru/media/today.tsv?page={i}"
        # Разбили строку на спиок, в каждом элементе которого храняться данные о редакции в строков виде.
        data_arr = requests.get(url_stat).text.split('\n')
        # Разбиваем каждую строку по символу "/", и вытаскиваем данные на 3 и 4 позиции(название и инфа соответственно).
        for edition in data_arr[1:-2]:
            name = repr(edition).split('\\')[2][1:]
            stat = int(repr(edition).split('\\')[3][1:])
            # Делаем имена редакций читабельными.
            for litteral in litterals:
                if litteral in name:
                    name = name.replace(litteral, '')
            # Добавляем данные в список в виде кортежа.
            today_reit.append((name, stat))

    return today_reit
