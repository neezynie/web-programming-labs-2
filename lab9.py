from flask import Blueprint, render_template, request, redirect, session, url_for  

lab9 = Blueprint('lab9', __name__)


@lab9.route('/lab9/', methods=['GET', 'POST'])
def main():
    if all(session.get(key) for key in ['name', 'age', 'gender', 'preference', 'preference']):
        return redirect(url_for('lab9.congratulation')) 
    if request.method == 'POST':
        session['name'] = request.form.get('name')
        return redirect(url_for('lab9.age'))  
    return render_template('lab9/index.html')

@lab9.route('/lab9/age', methods=['GET', 'POST'])
def age():
    if request.method == 'POST':
        session['age'] = request.form.get('age')
        return redirect(url_for('lab9.gender'))  
    return render_template('lab9/age.html')

@lab9.route('/lab9/gender', methods=['GET', 'POST'])
def gender():
    if request.method == 'POST':
        session['gender'] = request.form.get('gender')
        return redirect(url_for('lab9.preference')) 
    return render_template('lab9/gender.html')

# Страница для выбора предпочтений
@lab9.route('/lab9/preference', methods=['GET', 'POST'])
def preference():
    if request.method == 'POST':
        session['preference'] = request.form.get('preference')
        return redirect(url_for('lab9.detail'))  # Используем url_for
    return render_template('lab9/preference.html')

# Страница для уточнения предпочтений
@lab9.route('/lab9/detail', methods=['GET', 'POST'])
def detail():
    preference = session.get('preference')

    if request.method == 'POST':
        session['detail'] = request.form.get('detail')
        return redirect(url_for('lab9.congratulation'))  # Используем url_for

    if preference == 'вкусное':
        options = [('сладкое', 'Сладкое'), ('сытное', 'Сытное')]
    else:
        options = [('цветы', 'Цветы'), ('картина', 'Картина')]

    return render_template('lab9/detail.html', options=options)

# Страница с поздравлением и картинкой
@lab9.route('/lab9/congratulation')
def congratulation():
    name = session.get('name')
    age = int(session.get('age'))
    gender = session.get('gender')
    preference = session.get('preference')
    detail = session.get('detail')

    # Определение текста поздравления
    if gender == 'мужчина':
        greeting = f"Поздравляю тебя, {name}! Желаю, чтобы ты быстро вырос, был умным, сильным и счастливым."
    else:
        greeting = f"Поздравляю тебя, {name}! Желаю, чтобы ты быстро выросла, была умной, красивой и счастливой."

    # Определение картинки и дополнительного текста
    if preference == 'вкусное':
        if detail == 'сладкое':
            image = 'candy.jpg'
            gift = "Вот тебе подарок — мешочек конфет!"
        else:
            image = 'pizza.jpg'
            gift = "Вот тебе подарок — большая пицца!"
    else:
        if detail == 'цветы':
            image = 'flowers.jpg'
            gift = "Вот тебе подарок — красивый букет цветов!"
        else:
            image = 'art.jpg'
            gift = "Вот тебе подарок — красивая картина!"

    # Добавление текста в зависимости от возраста
    if age < 18:
        greeting += " Пусть твоя жизнь будет яркой и полной радости!"
    else:
        greeting += " Пусть твоя жизнь будет насыщенной и успешными начинаниями!"

    return render_template('lab9/congratulation.html', greeting=greeting, gift=gift, image=image)

@lab9.route('/lab9/restart')
def restart():
    for key in ['name', 'age', 'gender', 'preference', 'preference']:
        session.pop(key, None)
    return redirect(url_for('lab9.main'))  # Используем url_for