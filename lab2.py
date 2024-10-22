from flask import Blueprint, url_for, redirect, render_template_string, request, render_template

lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/a/')
def a():
    return 'со слэшем'

@lab2.route('/lab2/a')
def a2():
    return 'без слэша'

flower_list = ['роза','тюльпан','незабудка','ромашка']
@lab2.route('/lab2/flowers/<int:flower_id>')
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
@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
    global flower_list
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
@lab2.route('/lab2/add_flower')
def add_flower_error():
    return 'вы не задали имя цветка', 400
@lab2.route('/lab2/flowers/')
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
@lab2.route('/lab2/clear_flowers/')
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
@lab2.route('/lab2/add_all_flowers/')
def add_all_flowers():
    global flower_list
    flower_list = ['роза','тюльпан','незабудка','ромашка']
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлены все цветы</h1>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    <p><a href="/lab2/flowers/">Показать все цветы</a></p>
    </body>
</html>
'''
@lab2.route('/lab2/example')
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

@lab2.route('/lab2')
def lab2_view():
    return render_template('lab2.html')

@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)

@lab2.route('/lab2/calc/')
def redirect_to_default():
    return redirect(url_for('calculate', a=1, b=1))

@lab2.route('/lab2/calc/<int:a>')
def redirect_with_a(a):
    return redirect(url_for('calculate', a=a, b=1))

@lab2.route('/lab2/calc/<int:a>/<int:b>')
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

@lab2.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)

objects = [
    {
        "name": "Toyota Supra",
        "description": "Спортивный автомобиль с мощным двигателем.",
        "image": "toyota_supra.jpg"
    },
    {
        "name": "Ford Mustang",
        "description": "Американский купе с мощным мотором и агрессивным дизайном.",
        "image": "ford_mustang.jpg"
    },
    {
        "name": "Porsche 911",
        "description": "Классический немецкий спорткар с отличной управляемостью.",
        "image": "porshe_911.jpg"
    },
    {
        "name": "Nissan GT-R",
        "description": "Японский суперкар с впечатляющими характеристиками.",
        "image": "nissan_gtr.jpg"
    },
    {
        "name": "Chevrolet Corvette",
        "description": "Американский спорткар с мощным двигателем и динамичным дизайном.",
        "image": "chevrolet_corvette.jpg"
    }
]

@lab2.route('/lab2/objects')
def show_objects():
    return render_template('objects.html', objects=objects)