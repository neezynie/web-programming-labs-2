from flask import Flask, Blueprint, render_template, request, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
from os import path
import sqlite3
rgz = Blueprint('rgz', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='localhost',
            database='rgz',
            user='rgz_user',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@rgz.route('/rgz/')
def index():
    return render_template('rgz/index.html')

@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html')

    login = request.form.get('login')
    password = request.form.get('password')
    name = request.form.get('name')
    service_type = request.form.get('service_type')
    experience = request.form.get('experience')
    price = request.form.get('price')
    about = request.form.get('about')

    if not (login and password and name and service_type and experience and price):
        return render_template('rgz/register.html', error='Заполните все обязательные поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('rgz/register.html', error='Такой логин уже существует')

    # Сохранение пароля в открытом виде
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password, name, service_type, experience, price, about) VALUES (%s, %s, %s, %s, %s, %s, %s);",
                    (login, password, name, service_type, experience, price, about))
    else:
        cur.execute("INSERT INTO users (login, password, name, service_type, experience, price, about) VALUES (?, ?, ?, ?, ?, ?, ?);",
                    (login, password, name, service_type, experience, price, about))

    db_close(conn, cur)
    return redirect('/rgz/login')

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('rgz/login.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    user = cur.fetchone()

    # Проверка пароля напрямую
    if not user or user['password'] != password:
        db_close(conn, cur)
        return render_template('rgz/login.html', error='Неверный логин или пароль')

    session['login'] = login
    session['user_id'] = user['id']
    db_close(conn, cur)
    return redirect('/rgz/my_profile')

@rgz.route('/rgz/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/rgz/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    user = cur.fetchone()

    if request.method == 'POST':
        name = request.form.get('name')
        service_type = request.form.get('service_type')
        experience = request.form.get('experience')
        price = request.form.get('price')
        about = request.form.get('about')
        is_hidden = request.form.get('is_hidden') == '1'

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET name=%s, service_type=%s, experience=%s, price=%s, about=%s, is_hidden=%s WHERE login=%s;",
                        (name, service_type, experience, price, about, is_hidden, login))
        else:
            cur.execute("UPDATE users SET name=?, service_type=?, experience=?, price=?, about=?, is_hidden=? WHERE login=?;",
                        (name, service_type, experience, price, about, is_hidden, login))

        db_close(conn, cur)
        return redirect('/rgz/profile')

    db_close(conn, cur)
    return render_template('rgz/profile.html', user=user)

@rgz.route('/rgz/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('rgz/search.html')

    # Получаем параметры поиска из формы
    name = request.form.get('name')
    service_type = request.form.get('service_type')
    experience_min = request.form.get('experience_min')
    experience_max = request.form.get('experience_max')
    price_min = request.form.get('price_min')
    price_max = request.form.get('price_max')
    page = int(request.form.get('page', 1))

    conn, cur = db_connect()

    # Начальный запрос
    query = "SELECT * FROM users WHERE is_hidden=FALSE"
    params = []

    # Добавляем условия поиска
    if name:
        query += " AND name ILIKE %s"
        params.append(f"%{name}%")
    if service_type:
        query += " AND service_type=%s"
        params.append(service_type)
    if experience_min:
        query += " AND experience >= %s"
        params.append(experience_min)
    if experience_max:
        query += " AND experience <= %s"
        params.append(experience_max)
    if price_min:
        query += " AND price >= %s"
        params.append(price_min)
    if price_max:
        query += " AND price <= %s"
        params.append(price_max)

    # Добавляем пагинацию
    query += " ORDER BY id LIMIT 5 OFFSET %s;"
    params.append((page - 1) * 5)

    # Выполняем запрос
    cur.execute(query, tuple(params))
    users = cur.fetchall()

    db_close(conn, cur)

    # Возвращаем результаты поиска
    return render_template('rgz/search_results.html', users=users, page=page, name=name, service_type=service_type, experience_min=experience_min, experience_max=experience_max, price_min=price_min, price_max=price_max)

@rgz.route('/rgz/admin', methods=['GET', 'POST'])
def admin():
    # Проверка, что текущий пользователь - администратор
    if session.get('login') != 'admin':
        return redirect('/rgz/login')

    conn, cur = db_connect()

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        action = request.form.get('action')

        if action == 'delete':
            cur.execute("DELETE FROM users WHERE id=%s;", (user_id,))
        elif action == 'edit':
            return redirect(f'/rgz/admin/edit/{user_id}')

    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()

    db_close(conn, cur)
    return render_template('rgz/admin.html', users=users)
@rgz.route('/rgz/admin/edit/<int:user_id>', methods=['GET', 'POST'])
def admin_edit(user_id):
    # Проверка, что текущий пользователь - администратор
    if session.get('login') != 'admin':
        return redirect('/rgz/login')

    conn, cur = db_connect()

    if request.method == 'POST':
        # Обработка формы редактирования
        name = request.form.get('name')
        service_type = request.form.get('service_type')
        experience = request.form.get('experience')
        price = request.form.get('price')
        about = request.form.get('about')
        is_hidden = request.form.get('is_hidden') == '1'

        # Обновление данных пользователя
        cur.execute("UPDATE users SET name=%s, service_type=%s, experience=%s, price=%s, about=%s, is_hidden=%s WHERE id=%s;",
                    (name, service_type, experience, price, about, is_hidden, user_id))
        db_close(conn, cur)
        return redirect('/rgz/admin')

    # Получение данных пользователя
    cur.execute("SELECT * FROM users WHERE id=%s;", (user_id,))
    user = cur.fetchone()

    db_close(conn, cur)

    # Проверка, что пользователь существует
    if not user:
        return "Пользователь не найден", 404

    return render_template('rgz/admin_edit_profile.html', user=user)

@rgz.route('/rgz/logout')
def logout():
    session.pop('login', None)
    session.pop('user_id', None)
    return redirect('/rgz/login')

@rgz.route('/rgz/my_profile', methods=['GET'])
def my_profile():
    login = session.get('login')
    if not login:
        return render_template('rgz/my_profile.html', login="Анонимус", user=None)

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    user = cur.fetchone()
    db_close(conn, cur)

    return render_template('rgz/my_profile.html', login=login, user=user)

@rgz.route('/rgz/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    login = session.get('login')
    if not login:
        return redirect('/rgz/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    user = cur.fetchone()

    if request.method == 'POST':
        name = request.form.get('name')
        service_type = request.form.get('service_type')
        experience = request.form.get('experience')
        price = request.form.get('price')
        about = request.form.get('about')
        is_hidden = request.form.get('is_hidden') == '1'

        if not (name and service_type and experience and price):
            db_close(conn, cur)
            return render_template('rgz/edit_profile.html', error='Заполните все обязательные поля', user=user)

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET name=%s, service_type=%s, experience=%s, price=%s, about=%s, is_hidden=%s WHERE login=%s;",
                        (name, service_type, experience, price, about, is_hidden, login))
        else:
            cur.execute("UPDATE users SET name=?, service_type=?, experience=?, price=?, about=?, is_hidden=? WHERE login=?;",
                        (name, service_type, experience, price, about, is_hidden, login))

        db_close(conn, cur)
        return redirect('/rgz/my_profile')

    db_close(conn, cur)
    return render_template('rgz/edit_profile.html', user=user)

@rgz.route('/rgz/view_profiles', methods=['GET'])
def view_profiles():
    # Получаем параметр page из запроса, по умолчанию 1
    page = int(request.args.get('page', 1))

    conn, cur = db_connect()

    # Запрос с пагинацией (5 пользователей на странице)
    offset = (page - 1) * 5
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE is_hidden=FALSE ORDER BY id LIMIT 5 OFFSET %s;", (offset,))
    else:
        cur.execute("SELECT * FROM users WHERE is_hidden=FALSE ORDER BY id LIMIT 5 OFFSET ?;", (offset,))

    users = cur.fetchall()
    db_close(conn, cur)

    return render_template('rgz/view_profiles.html', users=users, page=page)




