from flask import Blueprint, render_template, request, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
lab6 = Blueprint('lab6', __name__)

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

@lab6.route('/lab6/')
def main():
    login = session.get('login')  
    return render_template('lab6/lab6.html', login=login)  

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():  
    data = request.json
    id = data['id']
    if data['method'] == 'info':
        conn, cur = db_connect()
        cur.execute("SELECT * FROM offices;")
        offices = cur.fetchall()
        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Method not found'
            },
            'id': id
        }
    if data['method'] == 'booking':
        office_number = data['params']
        conn, cur = db_connect()
        cur.execute("SELECT tenant FROM offices WHERE number = %s;", (office_number,))
        tenant = cur.fetchone()['tenant']
        if tenant:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 2,
                    'message': 'Already booked'
                },
                'id': id
            }
        cur.execute("UPDATE offices SET tenant = %s WHERE number = %s;", (login, office_number))
        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }
    if data['method'] == 'cancellation':
        office_number = data['params']
        conn, cur = db_connect()
        cur.execute("SELECT tenant FROM offices WHERE number = %s;", (office_number,))
        tenant = cur.fetchone()['tenant']
        if tenant != login:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'You are not the owner of this booking'
                },
                'id': id
            }
        cur.execute("UPDATE offices SET tenant = '' WHERE number = %s;", (office_number,))
        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }

@lab6.route('/lab6/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab6/lab6_login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    session['login'] = login
    return redirect('/lab6/')

@lab6.route('/lab6/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab6/lab6_register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    session['login'] = login
    return redirect('/lab6/')

@lab6.route('/lab6/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab6/')