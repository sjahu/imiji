#!python3

from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('config.py')

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/')
    def get_index():
        return app.send_static_file('index.html')

    return app
