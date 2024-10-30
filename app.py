from flask import Flask, url_for, redirect, render_template_string, request, render_template
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
app = Flask(__name__)
app.secret_key = "секретно-секретный секрет"
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
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
            <p>К сожалению, запрашиваемая вами страница не найдена.</p>
            <img src="{image_path}" alt="404 Image">
            <p><a href="/">Вернуться на главную</a></p>
        </body>
    </html>
    """
    return render_template_string(html), 404

@app.errorhandler(500)
def internal_server_error(err):
    css_path = url_for('static', filename='style.css')
    
    html = f"""
    <!doctype html>
    <html>
        <head>
            <title>Ошибка 500</title>
            <link rel="stylesheet" href="{css_path}">
        </head>
        <body>
            <h1>Ошибка 500</h1>
            <p>К сожалению, на сервере произошла ошибка. Пожалуйста, попробуйте позже.</p>
            <p><a href="/">Вернуться на главную</a></p>
        </body>
    </html>
    """
    return render_template_string(html), 500

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

