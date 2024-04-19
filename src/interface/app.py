import json

from tools.sidebar_placeholder_generator import sites as sidebar_placeholder

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


@app.route('/chart/<path:value>')
def main_view(value):
    redirect_url = request.args.get('redirect')
    if redirect_url:
        return redirect(f'/chart/{redirect_url}', 301)
    # search = request.args.get('search', '')

    # Временное решение, пока не готова back-end часть
    db = sqlite3.connect('test_db/data.db')
    cur = db.cursor()
    cur.execute(f""" SELECT * from data """)
    data = cur.fetchall()

    table_data = enumerate(data, start=1)
    data = {date[:-5]: value for date, value in data}
    json_data = json.dumps(data)

    return render_template('main.html',
                           active='chart',
                           site=value,
                           chart_data=json_data,
                           table_data=table_data,
                           left_table=sidebar_placeholder)


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'

    return response


if __name__ == '__main__':
    app.run(port=9999)
