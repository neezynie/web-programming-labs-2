from flask import Blueprint, render_template, request, redirect, session
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='gleb_kubrakov_knowledge_base',
        user='gleb_kubrakov_knowledge_base',
        password='123'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def db_close(conn, cur):
    cur.close()
    conn.close()

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login and password):
        return render_template('lab5/login.html', error='Заполните все поля')
    
    conn, cur = db_connect()
    cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    password_hash = generate_password_hash(password)
    
    conn, cur = db_connect()
    cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')
    
    cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    conn.commit()
    db_close(conn, cur)
    
    return render_template('lab5/success_register.html', login=login)

@lab5.route('/lab5/list')
def list_articles():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM articles;")
    articles = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/list.html', articles=articles)

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create_article():
    if request.method == 'GET':
        return render_template('lab5/create.html')
    
    title = request.form.get('title')
    content = request.form.get('content')
    
    if not (title and content):
        return render_template('lab5/create.html', error='Заполните все поля')
    
    conn, cur = db_connect()
    cur.execute("INSERT INTO articles (title, content) VALUES (%s, %s);", (title, content))
    conn.commit()
    db_close(conn, cur)
    
    return redirect('/lab5/list')