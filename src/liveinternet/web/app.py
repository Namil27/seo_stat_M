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
    lines = []
    for rank, link in enumerate(api_rating, start=1):
        if api_rating[link]:
            visitors = format(int(api_rating[link]), ',').replace(',', ' ')
        else:
            visitors = '. . .'
        line = {'rank': rank, 'link': link, 'visitors': visitors}
        lines.append(line)

    search = request.args.get('search')
    if search:
        sidebar = [i for i in lines if search in i['link']]
    else:
        sidebar = lines
        search = ''

    if value not in [i['link'] for i in lines]:
        return render_template(template_name_or_list='not_found.html',
                               site=value,
                               left_table=sidebar,
                               search_text=search)

    api_data = requests.get('http://23.111.123.4:8000/data/' + value).json()
    table_api_data = []
    for index, date in enumerate(api_data, start=1):
        if api_data[date]:
            visitors = format(int(api_data[date]), ',').replace(',', ' ')
        else:
            visitors = '-'
        line = {'index': index, 'date': date, 'visitors': visitors}
        table_api_data.append(line)
    print(table_api_data)
    chart_api_data = {key[5:]: value for key, value in api_data.items() if value is not None}
    print(api_data)
    print(chart_api_data)
    json_data = json.dumps(api_data)

    return render_template(template_name_or_list='main.html',
                           site=value,
                           chart_data=json.dumps(chart_api_data),
                           table_data=table_api_data,
                           left_table=sidebar,
                           search_text=search)


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'

    return response


if __name__ == '__main__':
    app.run(port=9999, debug=True)
