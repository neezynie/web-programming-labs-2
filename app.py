from flask import Flask, url_for, redirect
app= Flask(__name__)
@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404
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
            </ul>
            <footer>
                <p>ФИО: Кубраков Глеб Евгеньевич</p>
                <p>Группа: ФБИ-22</p>
                <p>Курс: 3</p>
                <p>Год: 2024</p>
            </footer>
        </body>
    </html>
    """
@app.route("/lab1")
def lab1():
    return """
    <!doctype html>
    <html>
        <head>
            <title>Лабораторная 1</title>
        </head>
        <body>
            <h1>Лабораторная 1</h1>
            <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
            <a href="/">Вернуться на главную</a>
        </body>
    </html>
    """
@app.route("/lab1/web")
def start():
    return """<!doctype html>
        <html> 
            <body>
                <h1>web-сервер на flask</h1>
                <a href="/author">author</a>
            </body> 
        </html>""", 200, {
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
                <a href="/web">web</a>
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

if __name__ == '__main__':
    app.run(debug=True)
@app.route("/lab1/info")
def info():
    return redirect("/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201