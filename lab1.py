from flask import Blueprint, url_for, redirect, render_template_string, request

lab1 = Blueprint('lab1', __name__)

@lab1.route("/lab1")
def lab1_view():
    routes = [
        ("/", "Главная"),
        ("/index", "Главная (index)"),
        ("/lab1", "Первая лабораторная"),
        ("/error/400", "Ошибка 400"),
        ("/error/401", "Ошибка 401"),
        ("/error/402", "Ошибка 402"),
        ("/error/403", "Ошибка 403"),
        ("/error/405", "Ошибка 405"),
        ("/error/418", "Ошибка 418"),
        ("/trigger_error", "Вызвать ошибку на сервере"),
        ("/about", "О Flask"),
        ("/lab1/web", "web-server"),
        ("/lab1/author", "Author"),
        ("/lab1/oak", "OAK"),
        ("/lab1/counter", "счетчик"),
        ("/lab1/reset_counter", "Сбросить счётчик"),
        ("/lab1/info", "Информация"),
        ("/lab1/created", "Создано успешно")
    ]
    
    route_links = "\n".join([f'<li><a href="{route}">{name}</a></li>' for route, name in routes])
    
    return f"""
    <!doctype html>
    <html>
        <head>
            <title>Лабораторная 1</title>
        </head>
        <body>
            <h1>Лабораторная 1</h1>
            <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
            <a href="/">Вернуться на главную</a>
            <h2>Список роутов</h2>
            <ul>
                {route_links}
            </ul>
        </body>
    </html>
    """

@lab1.route("/lab1/web")
def start():
    return """<!doctype html>
        <html> 
            <body>
                <h1>web-сервер на flask</h1>
                <a href="/lab1/author">author</a>
            </body> 
        </html>""" , 200, {
            "X-Server": "sample",
            'Content-Type':'text/plain; charset=utf-8'
            }


@lab1.route("/lab1/author")
def author():
    name="Кубраков Глеб Евгеньевич"
    group= "ФБИ-22"
    faculty="ФБ"
    return """<!doctype html>
        <html> 
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body> 
        </html>"""


@lab1.route("/lab1/oak")
def oak():
    path = url_for("static",  filename="oak.jpg")
    path2 = url_for("static", filename="lab1.css")
    return '''
    <!doctype html>
    <html> 
        <head>
        <link href="'''+ path2 +'''" rel="stylesheet">
        </head>
        <body>
            <h1>Дуб</h1>
            <img src="''' + path + '''">
        </body> 
    </html>
    '''


count = 0
@lab1.route('/lab1/counter')
def counter():
    global count
    count+=1
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
    <br>
        <a href="/lab1/reset_counter">Сбросить счётчик</a>
    </body>
</html>
'''


@lab1.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <body>
        Счётчик сброшен.
        <br>
        <a href="/lab1/counter">Вернуться к счётчику</a>
    </body>
</html>
'''


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@lab1.route("/lab1/created", methods=['GET', 'POST'])
def created():
    global resource_created
    if request.method == 'POST':
        if not resource_created:
            resource_created = True
            return '''
            <!doctype html>
            <html>
                <head>
                    <title>Успешно: ресурс создан</title>
                </head>
                <body>
                    <h1>Успешно: ресурс создан</h1>
                    <a href="/lab1/resource">Вернуться к ресурсу</a>
                </body>
            </html>
            ''', 201
        else:
            return '''
            <!doctype html>
            <html>
                <head>
                    <title>Отказано: ресурс уже создан</title>
                </head>
                <body>
                    <h1>Отказано: ресурс уже создан</h1>
                    <a href="/lab1/resource">Вернуться к ресурсу</a>
                </body>
            </html>
            ''', 400
    else:
        return redirect(url_for('resource'))


@lab1.route("/lab1/delete", methods=['GET', 'POST'])
def delete():
    global resource_created
    if request.method == 'POST':
        if resource_created:
            resource_created = False
            return '''
            <!doctype html>
            <html>
                <head>
                    <title>Успешно: ресурс удалён</title>
                </head>
                <body>
                    <h1>Успешно: ресурс удалён</h1>
                    <a href="/lab1/resource">Вернуться к ресурсу</a>
                </body>
            </html>
            ''', 200
        else:
            return '''
            <!doctype html>
            <html>
                <head>
                    <title>Отказано: ресурс отсутствует</title>
                </head>
                <body>
                    <h1>Отказано: ресурс отсутствует</h1>
                    <a href="/lab1/resource">Вернуться к ресурсу</a>
                </body>
            </html>
            ''', 400
    else:
        return redirect(url_for('resource'))

from werkzeug.security import generate_password_hash

# Генерация хеша пароля
password = "admin"
hashed_password = generate_password_hash(password)
print(hashed_password)