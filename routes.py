"""
Подпрограмма содержащая маршруты и обработку запросов.
"""


from flask import Flask, render_template
from flask import Blueprint, request, jsonify
import random
import json


main_routes = Blueprint('main_routes', __name__)


with open('settings.json', "r" , encoding='utf-8') as json_file:
    settings = json.load(json_file)


@main_routes.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method =='POST':
        settings["user_data"] = request.form.to_dict()
        with open('settings.json', "w", encoding='utf-8') as write_file:
            json.dump(settings, write_file)
    return render_template('page_main.html', settings=settings)


@main_routes.route('/_')
def hello_world_():
    data = {"data": round(5*random.random(), 4)}
    return jsonify(data)