from flask import Flask, render_template, request, redirect, send_from_directory 
from db import db_session, Urls
from datetime import datetime
import requests
import uuid
import validators


app = Flask(__name__, static_folder='static') 


def date_string():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def save_url_info(url, short_link, date):
    db_session.add(Urls(None, url, short_link, date))
    db_session.commit()
    db_session.close()
    return short_link


def short_link_generation():
    short_link = ''
    alpha = {'1': 'A',
             '2': 'B',
             '3': 'C',
             '4': 'E',
             '5': 'H',
             '6': 'K',
             '7': 'M',
             '8': 'O',
             '9': 'P',
             '0': 'T'}
    for row in str(hash(str(uuid.uuid1())) % 100000000):
        short_link = (alpha.get(row)) + short_link
    return short_link


def get_input_urls(link):
    url_link = [url.input_url for url in Urls.query.filter(Urls.short_link == '{link}'.format(link=link))]
    if url_link != []:
        return url_link[0]
    else:
        return False


def path_validator(path):
    flag = 1
    for row in path:
        if row not in 'ABCEHKMOPT':
            flag = 1
            break
        else:
            flag = 0
    if flag == 0:
        if get_input_urls(path):
            return get_input_urls(path)
    else:
        return False

def url_validator(url):
    if validators.url(url) == True:
        return False
    else:
        return True

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/', methods=['GET', 'POST'])
def main():
    link = ''
    status = True
    if request.method == 'POST':
        url = request.form['url']
        status = url_validator(url)
        if status == False:
            link = short_link_generation()
            save_url_info(url, link, date_string())
            return render_template('index.html', status=status, link=link)
        else:
            return render_template('index.html', status=status, link=link)
    return render_template('index.html')


@app.route('/<path>')
def redirect_link(path):
    urls_path = path_validator(path)
    if urls_path:
        return redirect('{urls_path}'.format(urls_path=urls_path), code=302) 
    else:
        return render_template('index.html', code=404)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
