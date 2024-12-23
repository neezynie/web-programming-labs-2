
from flask import Blueprint, render_template, request, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
from db.models import users, articles
from db import db
from flask import Flask
from db.models import db
from flask_login import login_user, login_required, current_user

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html', login=session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='localhost',
            database='gleb_kubrakov_knowledge_base',
            user='gleb_kubrakov_knowledge_base',
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


@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                               error = 'Такой пользователь уже существует')
    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/lab8/')

    if not (login and password_form):
        return render_template('lab8/register.html', error='Заполните все поля')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login, ))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab8/register.html', error='такой логин уже существует')
    
    password_hash = generate_password_hash(password_form)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))
    db_close(conn, cur)
    return render_template('lab8/login.html', login=login)


@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    user = users.query.filter_by(login = login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember = False)
            return redirect('/lab8/')
    return render_template('/lab8/login.html',
                           error = 'Ошибка входа: логин и/или пароль неверны')
    if not (login and password_form):
        return render_template('lab8/login.html', error='Заполните все поля')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    user = cur.fetchone()

    if not user or not check_password_hash(user['password'], password_form):
        db_close(conn, cur)
        return render_template('lab8/login.html', error="Пользователь и/или пароль введены неверно!")
    
    session['login'] = login
    session['login_id'] = user['id']  
    db_close(conn, cur)
    return render_template('lab8/success_login.html', login=login)



@lab8.route('/lab8/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab8/login')
    
    if request.method == 'GET':
        return render_template('/lab8/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == '1'

    if not (title and article_text):
        return render_template('/lab8/create_article.html', error='Введите текст и название статьи!')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    
    login_id = cur.fetchone()['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles(user_id, title, article_text, is_public) VALUES (%s, %s, %s, %s);", (login_id, title, article_text, is_public))
    else:
        cur.execute("INSERT INTO articles(login_id, title, article_text, is_public) VALUES (?, ?, ?, ?);", (login_id, title, article_text, is_public))
    
    db_close(conn, cur)
    return redirect('/lab5')


@lab8.route('/lab8/list')
def list():
    login = session.get('login')
    
    conn, cur = db_connect()

    sqllite = False
    is_admin = False

    if login == 'admin':
        is_admin = True
    user_id = None
    if login:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
            sqllite = True

        user = cur.fetchone()
        user_id = user['id'] if user else None

    if current_app.config['DB_TYPE'] == 'postgres':
        query = """
            SELECT articles.*, users.login as creator_login 
            FROM articles 
            JOIN users ON articles.user_id = users.id
        """
    else:
        query = """
            SELECT articles.*, users.login as creator_login 
            FROM articles 
            JOIN users ON articles.login_id = users.id
        """
    conditions = []
    params = []

    if login:
        if current_app.config['DB_TYPE'] == 'postgres':
            conditions.append("(articles.is_public = TRUE OR articles.user_id = %s)")
        else:
            conditions.append("(articles.is_public = TRUE OR articles.login_id = ?)")
        params.append(user_id)
    else:
        conditions.append("articles.is_public = TRUE")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY articles.is_favorite DESC, articles.id DESC;"

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(query, tuple(params) if params else ())
    else:
        cur.execute(query, tuple(params) if params else ())

    articles = cur.fetchall()

    db_close(conn, cur)

    return render_template('/lab8/articles.html', articles=articles, filter_type='all', sqllite=sqllite, is_admin=is_admin)


@lab8.route('/lab8/articles/', methods=['GET', 'POST'])
def article_list():
    if current_user.is_authenticated:
        search_query = request.form.get('query', '').strip() if request.method == 'POST' else ''
        my_articles = articles.query.filter_by(login_id=current_user.id).all()
        public_articles = articles.query.filter(
            (articles.is_public == True) & (articles.login_id != current_user.id)
        ).all()

        results = None
        if search_query:
            results = articles.query.filter(
                (articles.title.ilike(f'%{search_query}%') | articles.article_text.ilike(f'%{search_query}%')) &
                ((articles.is_public == True) | (articles.login_id == current_user.id))
            ).all()

        return render_template(
            'lab8/articles.html',
            my_articles=my_articles,
            public_articles=public_articles,
            search_query=search_query,
            results=results
        )
    else:
        search_query = request.form.get('query', '').strip() if request.method == 'POST' else ''
        results = None
        if search_query:
            results = articles.query.filter(
                (articles.title.ilike(f'%{search_query}%') | articles.article_text.ilike(f'%{search_query}%')) &
                ((articles.is_public == True))
            ).all()
        public_articles = articles.query.filter(
            (articles.is_public == True)
        ).all()
        return render_template(
            'lab8/articles.html',
            public_articles=public_articles,
            search_query=search_query,
            results=results
        )


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab8/login')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))
    
    article = cur.fetchone()
    if not article:
        db_close(conn, cur)
        return redirect('/lab8/list')

    if request.method == 'POST':
        new_title = request.form.get('title')
        new_article_text = request.form.get('article_text')
        is_public = request.form.get('is_public') == '1'

        if not (new_title and new_article_text):
            db_close(conn, cur)
            return render_template('/lab8/edit_article.html', error='Заполните все поля!', article=article)

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE articles SET title=%s, article_text=%s, is_public=%s WHERE id=%s;", (new_title, new_article_text, is_public, article_id))
        else:
            cur.execute("UPDATE articles SET title=?, article_text=?, is_public=? WHERE id=?;", (new_title, new_article_text, is_public, article_id))

        db_close(conn, cur)
        return redirect('/lab8/list')

    db_close(conn, cur)
    return render_template('/lab8/edit_article.html', article=article)


@lab8.route('/lab8/favorite/<int:article_id>', methods=['POST'])
def favorite(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab8/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
    user_id = cur.fetchone()['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id = %s;", (article_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE id = ?;", (article_id,))

    article = cur.fetchone()

    if current_app.config['DB_TYPE'] == 'postgres':
        if article:
            if article['is_favorite'] == False:
                cur.execute("UPDATE articles SET is_favorite = TRUE WHERE id = %s;", (article_id,))
            else:
                cur.execute("UPDATE articles SET is_favorite = FALSE WHERE id = %s;", (article_id,))
    else:
        if article:
            if article['is_favorite'] == False:
                cur.execute("UPDATE articles SET is_favorite = TRUE WHERE id = ?;", (article_id,))
            else:
                cur.execute("UPDATE articles SET is_favorite = FALSE WHERE id = ?;", (article_id,))

    db_close(conn, cur)
    return redirect('/lab8/list')


@lab8.route('/lab8/users')
def list_users():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users;")
    else:
        cur.execute("SELECT login FROM users;")
    
    users = cur.fetchall()
    db_close(conn, cur)
    return render_template('/lab5/users.html', users=users)


@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
def delete(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab8/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
    user_id = cur.fetchone()['id']

    cur.execute("SELECT * FROM articles WHERE id = %s;", (article_id,))
    article = cur.fetchone()

    if article and article['user_id'] == user_id:
        cur.execute("DELETE FROM articles WHERE id = %s;", (article_id,))
    
    db_close(conn, cur)
    return redirect('/lab8/list')
