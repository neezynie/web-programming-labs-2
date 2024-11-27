
from flask import Blueprint, render_template, request, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab6 = Blueprint('lab6', __name__)

offices = []
for i in range(1,11):
    offices.append({"number":i,"tenant":""})
@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')
@lab6.route('/lab6/json-rpc-api/', methods = ['POST'])
def api():  
    data = request.json
    id = data['id']
    if data['method'] == 'info':
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
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Already booked'
                        },
                        'id': id
                    }
                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }
    if data['method'] == 'cancellation':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                            'message': 'You are not the owner of this booking'
                        },
                        'id': id
                    }
                office['tenant'] = ''
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