"""
Основное приложение Flask.
"""


from flask import Flask, render_template
from routes import main_routes
import os


app = Flask(__name__)
app.register_blueprint(main_routes)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
    
    