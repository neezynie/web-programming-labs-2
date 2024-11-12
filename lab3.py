from flask import Blueprint, url_for, redirect, render_template_string, request, render_template, make_response

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.form.get('user')
    age = request.form.get('age')
    sex = request.form.get('sex')
        # Проверка на пустое значение поля "user"
    if user == '':
            errors['user'] = 'Заполните поле!'

        # Проверка на пустое значение поля "age"
    if not age:
            errors['age'] = 'Заполните поле!'

    if not errors:
            return render_template('lab3/form1.html', user=user, age=age, sex=sex)

    return render_template('lab3/form1.html', errors=errors)

@lab3.route('/lab3/', endpoint='lab3_index')
def lab():
    name = request.cookies.get('name') or 'аноним'  # По умолчанию "аноним", если имя не установлено
    age = request.cookies.get('age') or 'неизвестный'  # По умолчанию "неизвестный", если возраст не установлен
    name_color = request.cookies.get('name_color') or 'black'  # По умолчанию черный цвет, если цвет не установлен
    return render_template('lab3/lab3.html', name=name, age=age, name_color=name_color)

@lab3.route('/lab3/cookie', endpoint='set_cookie')
def cookie():
    resp = make_response("Установка cookie", 200)
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '30', max_age=5)  # Установка возраста
    resp.set_cookie('name_color', 'blue', max_age=5)  # Установить цвет на синий на 5 секунд
    return resp

@lab3.route('/lab3/del_cookie', endpoint='delete_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')  # Удаление возраста
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/order', methods=['GET'])
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay', methods=['GET'])
def pay():
    price = 0
    drink = request.args.get("drink")
    if drink == "cofee":
        price = 120
    elif drink == "black_tea":
        price = 80  
    else:
        price= 70
    if request.args.get('milk') == 'on':
            price += 30
    if request.args.get('sugar') == 'on':
            price += 10

    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success', methods=['GET'])
def success():
    price = request.args.get("price")
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings', methods=['GET'])
def settings():
    print(f"Request method: {request.method}")  # Добавьте эту строку для отладки
    color = request.args.get("color")
    font_size = request.args.get("font_size")
    font_family = request.args.get("font_family")
    
    if color or font_size or font_family:
        resp = make_response(redirect('/lab3/settings'))
        
        if color:
            resp.set_cookie('color', color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_family:
            resp.set_cookie('font_family', font_family)
        
        return resp

    color = request.cookies.get('color')
    font_size = request.cookies.get('font_size')
    font_family = request.cookies.get('font_family')
    
    return render_template('lab3/settings.html', color=color, font_size=font_size, font_family=font_family)

@lab3.route('/lab3/clear_cookies', endpoint='clear_cookies')
def clear_cookies():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_family')
    resp.delete_cookie('text_color')
    return resp

@lab3.route('/lab3/ticket', methods=['GET'])
def ticket():
    if request.method == 'GET':
        fio = request.args.get('fio')
        bunk = request.args.get('bunk')
        bedclothes = request.args.get('bedclothes')
        baggage = request.args.get('baggage')
        age = request.args.get('age')
        departure = request.args.get('departure')
        destination = request.args.get('destination')
        date = request.args.get('date')
        insurance = request.args.get('insurance')

        errors = {}

        if not fio:
            errors['fio'] = 'Заполните поле ФИО'
        if not bunk:
            errors['bunk'] = 'Выберите полку'
        if not age:
            errors['age'] = 'Заполните поле возраста'
        elif not (1 <= int(age) <= 120):
            errors['age'] = 'Возраст должен быть от 1 до 120 лет'
        if not departure:
            errors['departure'] = 'Заполните поле пункта выезда'
        if not destination:
            errors['destination'] = 'Заполните поле пункта назначения'
        if not date:
            errors['date'] = 'Заполните поле даты поездки'

        if errors:
            return render_template('lab3/ticket_form.html', errors=errors)

        base_price = 700 if int(age) < 18 else 1000
        if bunk in ['нижняя', 'нижняя боковая']:
            base_price += 100
        if bedclothes:
            base_price += 75
        if baggage:
            base_price += 250
        if insurance:
            base_price += 150

        ticket_type = 'Детский билет' if int(age) < 18 else 'Взрослый билет'

        return render_template('lab3/ticket_result.html', fio=fio, bunk=bunk, bedclothes=bedclothes, baggage=baggage, age=age, departure=departure, destination=destination, date=date, insurance=insurance, price=base_price, ticket_type=ticket_type)

    return render_template('lab3/ticket_form.html')