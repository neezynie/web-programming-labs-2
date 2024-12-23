from flask import Flask, url_for, redirect, render_template, abort, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from db.models import users
from flask_login import LoginManager
from db import db
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9

import os
from os import path
app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = "секретно-секретный секрет"
@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))
login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(login_id):
    return users.query.get(int(login_id))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret_secret_key')

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'gleb_kubrakov_orm'
    db_user = 'gleb_kubrakov_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, 'gleb_kubrakov_orm.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'


db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)
@app.errorhandler(404)
def not_found(err):
    image_path = url_for('static', filename='404.jpg')
    css_path = url_for('static', filename='style.css')
    
    html = f"""
    <!doctype html>
    <html>
        <head>
            <title>Ошибка 404</title>   
            <link rel="stylesheet" href="{css_path}">
        </head>
        <body>
            <h1>Ошибка 404</h1>
            <p>К сожалению, запрашиваемая вами страница не найдена!!!.</p>
            <img src="{image_path}" alt="404 Image">
            <p><a href="/">Вернуться на главную</a></p>
        </body>
    </html>
    """
    return render_template_string(html), 404

@app.route("/")

@app.route("/index")
def index():
    return """
    <!doctype html>
    <html>
        <head>
            <title>НГТУ, ФБ, Лабораторные работы</title>
            <link rel="stylesheet" href="{{ url_for('static', filename='lab1/main.css') }}">
        </head>
        <body>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
                <li><a href="/lab2">2 лабораторная</a></li>
                <li><a href="/lab3/">3 лабораторная</a></li>
                <li><a href="/lab4/">4 лабораторная</a></li>
                <li><a href="/lab5/">5 лабораторная</a></li>
                <li><a href="/lab6/">6 лабораторная</a></li>
                <li><a href="/lab7/">7 лабораторная</a></li>
                <li><a href="/lab8/">8 лабораторная</a></li>
                <li><a href="/lab9/">9 лабораторная</a></li>
            </ul>
            <footer>
                <p>ФИО: Кубраков Глеб Евгеньевич</p>
                <p>Группа: ФБИ-22</p>
                <p>Курс: 2</p>
                <p>Год: 2023</p>
            </footer>
        </body>
    </html>
    """

    global resource_created
    status = "ресурс создан" if resource_created else "ресурс ещё не создан"
    return f"""
    <!doctype html>
    <html>
        <head>
            <title>Статус ресурса</title>
        </head>
        <body>
            <h1>Статус ресурса: {status}</h1>
            <form action="{url_for('created')}" method="post">
                <button type="submit">Создать ресурс</button>
            </form>
            <form action="{url_for('delete')}" method="post">
                <button type="submit">Удалить ресурс</button>
            </form>
        </body>
    </html>
    """
@app.route("/error/400")
def error_400():
    return "Bad Request", 400

@app.route("/error/401")
def error_401():
    return "Unauthorized", 401

@app.route("/error/402")
def error_402():
    return "Payment Required", 402

@app.route("/error/403")
def error_403():
    return "Forbidden", 403

@app.route("/error/405")
def error_405():
    return "Method Not Allowed", 405

@app.route("/error/418")
def error_418():
    return "I'm a teapot", 418

@app.route("/trigger_error")
def trigger_error():
    # Пример ошибки: деление на ноль
    return 1 / 0

@app.route("/about")
def about():
    image_path = url_for('static', filename='flask.png')
    css_path = url_for('static', filename='style.css')
    
    html = f"""
    <!doctype html>
    <html>
        <head>
            <title>О Flask</title>
            <link rel="stylesheet" href="{css_path}">
        </head>
        <body>
            <h1>О Flask</h1>
            <p>Flask — это микрофреймворк для создания веб-приложений на языке программирования Python. Он основан на Werkzeug, WSGI-утилите, и Jinja2, шаблонизаторе. Flask предоставляет минималистичный набор инструментов для создания веб-приложений, позволяя разработчикам гибко настраивать и расширять функциональность по мере необходимости.</p>
            <p>Одной из ключевых особенностей Flask является его простота и легкость в использовании. Он не навязывает разработчику определенную архитектуру или базу данных, что делает его идеальным выбором для небольших проектов и прототипирования. В то же время, Flask легко масштабируется для более сложных приложений благодаря поддержке расширений и плагинов.</p>
            <p>Flask широко используется в сообществе Python для создания различных веб-приложений, от простых блогов до сложных веб-сервисов. Его популярность обусловлена не только простотой и гибкостью, но и активной поддержкой со стороны сообщества разработчиков.</p>
            <img src="{image_path}" alt="Flask Logo">
            <p><a href="/">Вернуться на главную</a></p>
        </body>
    </html>
    """
    return render_template_string(html), 200, {
        'Content-Language': 'ru',
        'X-Custom-Header-1': 'Custom Value 1',
        'X-Custom-Header-2': 'Custom Value 2'
    }

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)  

