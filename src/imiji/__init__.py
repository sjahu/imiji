from flask import *
from datetime import datetime

from db import DB_Handler

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('config.py')

    db = DB_Handler(app.config)

    @app.route('/test')
    def hello():
        return "hello, world!"

    @app.route('/')
    def get_index():
        return app.send_static_file('index.html')


    @app.route('/api/v1.0/upload', methods=['POST'])
    def upload_image():
        """
        Upload an image. Request body must be json:

        {
          file: ... (REQUIED),
          description: ... (OPTIONAL)
        }
        """
        if not request.json or 'file' not in request.json:
            abort(400) # bad request
        try:
            id = db.insert_image(file = request.json['file'],
                                   description = request.json.get('description', ''),
                                   upload_date = datetime.now(),
                                   uploader_ip = request.remote_addr)
            return make_response(jsonify({'id': id}), 201) # created
        except Exception as e:
            return make_response(jsonify({'error': 'Failed to upload image', 'details': str(e)}), 500)

    @app.route('/api/v1.0/image/<id>')
    def get_image(id):
        """
        Retrieve an image by its ID
        """
        data = db.select_image(id)
        if data == None:
            abort(404)
        return make_response(jsonify(data), 200)

    return app
