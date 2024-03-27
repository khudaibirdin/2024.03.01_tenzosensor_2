"""
Основное приложение Flask.
"""


from flask import Flask, render_template
from routes import main_routes
from functions import func
import os, json
from apscheduler.schedulers.background import BackgroundScheduler
from classes.classes import GetModbusData

# создание экземпляра flask-приложения
app = Flask(__name__)
app.register_blueprint(main_routes)

# подъем данных с файла settings.json
with open('settings.json', "r" , encoding='utf-8') as json_file:
    settings = json.load(json_file)

# экземпляр класса для обработки modbus, он передается в scheduler
mb = GetModbusData(config=settings)

sched = BackgroundScheduler(daemon=True)
sched.add_job(func,'interval', seconds=0.1, args=[mb, app]) # также передается app, т.к. в функции происх. измен. переменной
sched.start()


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
