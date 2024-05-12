import json
import requests

from tools.sidebar_placeholder_generator import sites as sidebar_placeholder

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


@app.route('/')
def start():
    return render_template('start.html', left_table=sidebar_placeholder)


@app.route('/chart/<path:value>')
def main_view(value):
    api_rating = requests.get('http://23.111.123.4:8000/medias').json()
    lines = [{'rank': rank, 'link': link, 'visitors': api_rating[link]} for rank, link in enumerate(api_rating, start=1)]
    page = 'main.html'

    search = request.args.get('search')
    if search:
        sidebar = [i for i in lines if search in i['link']]
    else:
        sidebar = lines
    # Временное решение, пока не готова back-end часть
    db = sqlite3.connect('test_db/data.db')
    cur = db.cursor()
    cur.execute(f""" SELECT * from data """)
    data = cur.fetchall()

    table_data = enumerate(data, start=1)
    data = {date[:-5]: value for date, value in data}
    json_data = json.dumps(data)

    if value not in [i['link'] for i in lines]:
        page = 'not_found.html'

    return render_template(template_name_or_list=page,
                           site=value,
                           chart_data=json_data,
                           table_data=table_data,
                           left_table=sidebar,
                           search_text=search)


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'

    return response


if __name__ == '__main__':
    app.run(port=9999)
