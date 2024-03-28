"""
Основное приложение Flask.
"""


from flask import Flask, render_template
from appfiles.routes import main_routes
from appfiles.functions import func
import os, json
from apscheduler.schedulers.background import BackgroundScheduler
from appfiles.classes import GetModbusData
os.system('explorer "http://127.0.0.1:5000/"')

# создание экземпляра flask-приложения
app = Flask(__name__)
app.register_blueprint(main_routes)
app.config['max_pressure'] = 0
app.config['shift'] = 0
app.config['data_tenzo_raw_unpack'] = 0
app.config["data_massive"] = []
app.config["time_massive"] = []
# подъем данных с файла settings.json
with open('settings.json', "r" , encoding='utf-8') as json_file:
    app.config["settings"] = settings = json.load(json_file)

# экземпляр класса для обработки modbus, он передается в scheduler
mb = GetModbusData()
sched = BackgroundScheduler(daemon=True)
sched.add_job(func,'interval', seconds=0.1, args=[mb, app]) # также передается app, т.к. в функции происх. измен. переменной
sched.start()


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, threaded = True)
