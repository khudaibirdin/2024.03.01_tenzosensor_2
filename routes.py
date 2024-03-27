"""
Подпрограмма содержащая маршруты и обработку запросов.
"""


from flask import Flask, render_template
from flask import Blueprint, request, jsonify
from flask import current_app
import random
import json


main_routes = Blueprint('main_routes', __name__)


@main_routes.route('/', methods=['GET', 'POST'])
def main_page():
    """
    Обработчик основной страницы,
    открывает шаблон, при POST запросе (нажатие подтверждения изменений)
    записывает новые данные в файл settings.json
    """
    with open('settings.json', "r" , encoding='utf-8') as json_file:
        settings = json.load(json_file)
    if request.method =='POST': # при post-запросе считываются формы, записываются в файл
        settings = request.form.to_dict()
        with open('settings.json', "w", encoding='utf-8') as write_file:
            json.dump(settings, write_file)
    return render_template('page_main.html', settings=settings)


@main_routes.route('/_')
def main_page_():
    """
    Обработка ajax-запросов,
    передача на страницу актуальных данных
    """
    data = {"data": current_app.config['data']}
    return jsonify(data)
