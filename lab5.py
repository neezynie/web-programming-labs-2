from flask import Blueprint, render_template, request, redirect, session

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def index():
    username = session.get('username', 'anonymous')
    return render_template('lab5/lab5.html', username=username)

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    # Логика для обработки входа
    return redirect('/lab5/')

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    # Логика для обработки регистрации
    return redirect('/lab5/')

@lab5.route('/lab5/list')
def list_articles():
    # Логика для отображения списка статей
    return render_template('lab5/list.html')

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create_article():
    if request.method == 'GET':
        return render_template('lab5/create.html')
    
    # Логика для создания статьи
    return redirect('/lab5/list')