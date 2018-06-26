from flask import Flask, render_template, request, redirect
from db import db_session, Urls
from datetime import datetime
import requests
import logging


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


alpha = {'1': 'A',
         '2': 'B',
         '3': 'C',
         '4': 'D',
         '5': 'E',
         '6': 'H',
         '7': 'K',
         '8': 'M',
         '9': 'O',
         '0': 'P'}


def date_string():
    date = datetime.now()
    date = date.strftime('%Y-%m-%d %H:%M:%S')
    return date #'12.06.2018 17:30:59'


def gen_short_link():
    short_link = ''
    url_id = int(Urls.query.count()) + 1 # Берем кличество строк из БД
    for row in str(url_id):
        short_link = (alpha.get(row)) + short_link
    return short_link


def get_input_urls(link):
    url_link = [url.input_url for url in Urls.query.filter(Urls.short_link == '{link}'.format(link=link))]
    logging.info('url_link: %r', url_link)
    url_link = url_link[0]
    return url_link


def path_validator(path):
    valid_alpha = 'ABCDEHKMOP'
    flag = 3
    for row in path:
        if row not in valid_alpha:
            flag = 1
            break
        else:
            flag = 0
    if flag == 0:
        return get_input_urls(path)
    else:
        return 'no_valid'


def save_url(url):
    short_link = gen_short_link()
    date = date_string()
    link = Urls(None, url, short_link, date)
    db_session.add(link)
    db_session.commit()
    db_session.close()
    return short_link


@app.route('/', methods=['GET', 'POST'])
def main():
    urls = ''
    if request.method == 'POST':
        data = request.form['msg']
        urls = save_url(data)
    return render_template('index.html', urls=urls)
    

@app.route('/<path>')
def redirect_link(path):
    urls_path = path_validator(path)
    if urls_path == 'no_valid':
        return render_template('index.html', code=404)
    else:
        return redirect('{urls_path}'.format(urls_path=urls_path), code=302)
        

if __name__ == "__main__":
    app.run(debug=True)
