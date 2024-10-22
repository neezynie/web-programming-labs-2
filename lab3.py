from flask import Blueprint, url_for, redirect, render_template_string, request, render_template, make_response

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color') or 'black'  # Default to black if no color is set
    return render_template('lab3/lab3.html', name=name, name_color=name_color)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response("Установка cookie", 200)
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('name_color', 'blue', max_age=5)  # Set color to blue for 5 seconds
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('name_color')
    return resp