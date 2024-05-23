import re

import requests

from flask import Flask, render_template, request, jsonify
from unidecode import unidecode

app = Flask(__name__)


def normalize_text(text):
    # Приведение текста к нижнему регистру и удаление специальных символов
    normalized_text = unidecode(text).lower()
    normalized_text = re.sub(r'\W+', '', normalized_text)
    return normalized_text


def find_similar_entries(data_list, search_word):
    # Нормализация искомого слова
    normalized_search_word = normalize_text(search_word)

    # Поиск и вывод похожих словарей
    similar_entries = [
        entry for entry in data_list
        if normalized_search_word in normalize_text(entry['link'])
    ]
    return similar_entries


def sidebar_gen(search=''):
    """
    Генерирует список словарей, содержащих рейтинг, ссылку и количество посетителей для каждого медиа-сайта,
    основываясь на данных, полученных из внешнего API. Функция также поддерживает фильтрацию по поисковому запросу.

    Аргументы:
        search (str): Подстрока для фильтрации медиа-ссылок. Будут включены только ссылки, содержащие эту подстроку.
                      По умолчанию - пустая строка, что включает все ссылки.

    Возвращает:
        list: Список словарей, где каждый словарь содержит следующие ключи:
            - 'rank' (int): Рейтинг медиа-сайта, основанный на порядке в ответе API.
            - 'link' (str): Ссылка на медиа-сайт.
            - 'visitors' (str): Форматированное количество посетителей или '. . .', если количество посетителей недоступно.
    """
    api_rating = requests.get('http://23.111.123.4:8000/medias').json()

    lines = []
    for rank, link in enumerate(api_rating, start=1):
        if api_rating[link]:
            visitors = format(int(api_rating[link]), ',').replace(',', ' ')
        else:
            visitors = '. . .'
        line = {'rank': rank, 'link': link, 'visitors': visitors}
        lines.append(line)

    if search:
        sidebar = find_similar_entries(lines, search)
    else:
        sidebar = lines

    if not sidebar:
        sidebar = [{'rank': '', 'link': 'Упс... такого СМИ нет', 'visitors': ''}]

    return sidebar


@app.route('/')
def start():
    """
    Обрабатывает запрос на главную страницу, рендерит шаблон main.html и передает данные для боковой панели.

    Если в запросе присутствует параметр поиска, фильтрует данные боковой панели по этому параметру.

    Аргументы:
        search (str): Параметр запроса, используемый для фильтрации данных боковой панели. Если отсутствует, отображает все данные.

    Возвращает:
        Response: Отрендеренный шаблон main.html с переданными данными для боковой панели.

    Пример запроса:
        GET /?search=example

    Пример использования:
        - Пользователь открывает главную страницу и видит данные боковой панели.
        - Пользователь вводит параметр поиска в URL для фильтрации данных боковой панели.

    Примечания:
        - Функция использует функцию sidebar_gen для генерации данных боковой панели.
    """
    search = request.args.get('search')
    if not search:
        search = ''
    return render_template(template_name_or_list='main.html',
                           left_table=sidebar_gen(search), search_text=search)


@app.route('/content/<site>')
def content(site):
    """
    Возвращает данные о посещаемости для указанного сайта, полученные из внешнего API.

    Аргументы:
        site (str): Название сайта для получения данных о посещаемости.

    Возвращает:
        JSON: Объект JSON, содержащий данные о посещаемости сайта в формате:
            {
                "content": {
                    "дата1": значение1,
                    "дата2": значение2,
                    ...
                }
            }
            Если запрос к внешнему API завершился ошибкой, возвращается объект JSON с ключом "error" и сообщением об ошибке.

    HTTP-статус:
        200 OK: Успешный запрос и получение данных.
        500 Internal Server Error: Ошибка при запросе к внешнему API.

    Примеры:
        Успешный запрос:
        {
            "content": {
                "2024-05-10": 3111925,
                "2024-05-11": 3410835,
                ...
            }
        }

        Ошибка запроса:
        {
            "error": "Ошибка соединения"
        }
    """
    api_url = f'http://23.111.123.4:8000/data/{site}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return jsonify({'content': data})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    print(query)
    results = find_similar_entries(sidebar_gen(), query)
    return jsonify(results)


if __name__ == '__main__':
    app.run(port=9999, debug=False)
