from flask import Blueprint, render_template, escape, request

page = Blueprint('page', __name__, template_folder='templates')


@page.route('/')
def home():
    return render_template('home.html')
