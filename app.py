from flask import Flask, url_for, redirect, render_template_string, request, render_template

app = Flask(__name__)

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
        </head>
        <body>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
                <li><a href="/error/400">Ошибка 400</a></li>
                <li><a href="/error/401">Ошибка 401</a></li>
                <li><a href="/error/402">Ошибка 402</a></li>
                <li><a href="/error/403">Ошибка 403</a></li>
                <li><a href="/error/405">Ошибка 405</a></li>
                <li><a href="/error/418">Ошибка 418</a></li>
                <li><a href="/trigger_error">Вызвать ошибку на сервере</a></li>
                <li><a href="/about">О Flask</a></li>
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

@app.route("/lab1")
def lab1():
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

@app.route("/lab1/web")
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

@app.route("/lab1/author")
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

@app.route("/lab1/oak")
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
@app.route('/lab1/counter')
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

@app.route('/lab1/reset_counter')
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

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created", methods=['GET', 'POST'])
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
@app.route("/lab1/delete", methods=['GET', 'POST'])
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
@app.route("/lab1/resource")
def resource():
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
    app.run(debug=False, host='0.0.0.0', port=5000)  # Запуск без флага --debug и на всех интерфейсах

@app.route('/lab2/a/')
def a():
    return 'со слэшем'

@app.route('/lab2/a')
def a2():
    return 'без слэша'

flower_list = ['роза','тюльпан','незабудка','ромашка']
@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return 'такого цветка нет', 404
    else:
        flower_name = flower_list[flower_id]
        return f'''
<!doctype html>
<html>
    <body>
    <h1>Информация о цветке</h1>
    <p>Цветок: {flower_name}</p>
    <p><a href="/lab2/flowers/">Показать все цветы</a></p>
    </body>
</html>
'''
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка:  {name}  </p>
    <p>Всего цветов: {len(flower_list)} </p>
    <p>Полный список: {flower_list} </p>
    </body>
</html>
'''
@app.route('/lab2/add_flower')
def add_flower_error():
    return 'вы не задали имя цветка', 400
@app.route('/lab2/flowers/')
def list_flowers():
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Список всех цветов</h1>
    <p>Всего цветов: {len(flower_list)}</p>
    <ul>
        {"".join(f"<li>{f}</li>" for f in flower_list)}
    </ul>
    </body>
</html>
'''
@app.route('/lab2/clear_flowers/')
def clear_flowers():
    global flower_list
    flower_list = []
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Список цветов очищен</h1>
    <p>Все цветы были удалены.</p>
    <p><a href="/lab2/flowers/">Показать все цветы</a></p>
    </body>
</html>
'''
@app.route('/lab2/example')
def example():
    name = "Кубраков Глеб"
    group = "ФБИ-22"
    kyrs = "3 курс"
    laba = "Лабораторная работа 2"
    fruits=[
        {"name":"яблоки","price":100},
        {"name":"груши","price":120},
        {"name":"апельсины","price":80},
        {"name":"мандарины","price":95},
        {"name":"манго","price":321}
    ]
    return render_template('example.html', name=name, group=group, kyrs=kyrs, laba=laba, fruits=fruits)
@app.route('/lab2')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)
@app.route('/lab2/calc/')
def redirect_to_default():
    return redirect(url_for('calculate', a=1, b=1))

@app.route('/lab2/calc/<int:a>')
def redirect_with_a(a):
    return redirect(url_for('calculate', a=a, b=1))
@app.route('/lab2/calc/<int:a>/<int:b>')
def calculate(a, b):

    sum_result = a + b
    diff_result = a - b
    prod_result = a * b
    div_result = a / b 
    pow_result = a ** b


    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Калькулятор</title>
    </head>
    <body>
        <h1>Калькулятор</h1>
        <p>Сумма: { sum_result }</p>
        <p>Вычитание: { diff_result }</p>
        <p>Умножение: { prod_result }</p>
        <p>Деление: { div_result }</p>
        <p>Возведение в степень: { pow_result }</p>
    </body>
    </html>
    """
books = [
    {"author": "Джордж Оруэлл", "title": "1984", "genre": "Научная фантастика", "pages": 328},
    {"author": "Рэй Брэдбери", "title": "451 градус по Фаренгейту", "genre": "Научная фантастика", "pages": 158},
    {"author": "Федор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 671},
    {"author": "Джейн Остин", "title": "Гордость и предубеждение", "genre": "Роман", "pages": 432},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Фантастика", "pages": 480},
    {"author": "Габриэль Гарсиа Маркес", "title": "Сто лет одиночества", "genre": "Магический реализм", "pages": 448},
    {"author": "Эрих Мария Ремарк", "title": "Три товарища", "genre": "Роман", "pages": 480},
    {"author": "Антуан де Сент-Экзюпери", "title": "Маленький принц", "genre": "Философская сказка", "pages": 96},
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман", "pages": 1225},
    {"author": "Герман Мелвилл", "title": "Моби Дик", "genre": "Роман", "pages": 585},
]

@app.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)

