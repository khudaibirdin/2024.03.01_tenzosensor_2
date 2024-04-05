"""
Подпрограмма содержащая маршруты и обработку запросов.
"""


from flask import Flask, render_template
from flask import Blueprint, request, jsonify
from flask import current_app
import json
from appfiles.functions import make_document

main_routes = Blueprint('main_routes', __name__)


@main_routes.route('/', methods=['GET', 'POST'])
def main_page():
    """
    Обработчик основной страницы,
    открывает шаблон, при POST запросе (нажатие подтверждения изменений)
    записывает новые данные в файл settings.json
    """
    if request.method =='POST': # при post-запросе считываются формы, записываются в файл
        settings = request.form.to_dict()
        with open('settings.json', "w", encoding='utf-8') as write_file:
            json.dump(settings, write_file)
        current_app.config["settings"] = settings
    return render_template('page_main.html', settings=current_app.config["settings"])


@main_routes.route('/_')
def main_page_():
    """
    Обработка ajax-запросов,
    передача на страницу актуальных данных
    """
    data = {"data_tenzo": round(float(current_app.config['data_tenzo']), 2),
            "max_pressure": round(float(current_app.config['max_pressure']), 2),
            "data_pressure": round(float(current_app.config['data_pressure']), 2),
            "data_tenzo_raw": round(float(current_app.config['data_tenzo_raw']), 2)}
    return jsonify(data)


@main_routes.route('/correct_null')
def main_page_correct_null():
    """
    Обработка ajax-запросов,
    коррекция нуля
    """
    print("коррекция")
    if current_app.config["settings"]['tenzo_type'] == "200":
        current_app.config['shift'] = current_app.config['data_tenzo_raw_unpack'] - (-0.071)
    if current_app.config["settings"]['tenzo_type'] == "2000":
        current_app.config['shift'] = current_app.config['data_tenzo_raw_unpack'] - (-0.068)
    data = {"data_pressure": round(current_app.config['data_pressure'], 2),
            "data_tenzo": round(current_app.config['data_tenzo'], 2),
            "max_pressure": round(current_app.config['max_pressure'], 2)}
    return jsonify(data)


@main_routes.route('/sbros_max')
def main_page_sbros_max():
    """
    Обработка ajax-запросов,
    сброс макс. значения
    """
    print("Сброса максимума")
    current_app.config['max_pressure'] = 0
    data = {"data_pressure": round(current_app.config['data_pressure'], 2),
            "data_tenzo": round(current_app.config['data_tenzo'], 2),
            "max_pressure": round(current_app.config['max_pressure'], 2)}
    return jsonify(data)


@main_routes.route('/make_document')
def main_page_make_document():
    """
    Обработка ajax-запросов,
    создание документа
    """
    if len(current_app.config['data_massive']) > 0:
        make_document(current_app)
        with open('settings.json', "w", encoding='utf-8') as write_file:
            json.dump(current_app.config["settings"], write_file)
        current_app.config['max_pressure'] = 0
        data = {"data_pressure": round(current_app.config['data_pressure'], 2),
            "data_tenzo": round(current_app.config['data_tenzo'], 2),
            "max_pressure": round(current_app.config['max_pressure'], 2)}
        return jsonify(data)
    