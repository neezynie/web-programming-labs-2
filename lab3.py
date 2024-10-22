from flask import Blueprint, url_for, redirect, render_template_string, request, render_template

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab3_index():
    return render_template('lab3/lab3.html')

@lab3.route('/lab3/cookie')
def lab3_cookie():
    return "This is the cookie page for lab3."