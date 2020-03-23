from flask import *
from datetime import datetime
from base64 import b64encode, b64decode
from io import BytesIO

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
          file: ... (REQUIED) (base64 encoded),
          description: ... (OPTIONAL)
        }
        """
        if not request.json or 'file' not in request.json:
            abort(400) # bad request
        try:
            id = db.insert_image(file = b64decode(request.json['file']),
                                 description = request.json.get('description', ''),
                                 date = datetime.now(),
                                 uploader_ip = request.remote_addr)
            return make_response(jsonify({'id': id}), 201) # created
        except Exception as e:
            return make_response(jsonify({'error': 'Failed to upload image', 'details': str(e)}), 500)

    @app.route('/api/v1.0/image/<id>', methods=['GET'])
    def get_image(id):
        """
        Retrieve an image by its ID

        Returns json response { id, file, description, upload_date }
        """
        try:
            data = db.select_image(id)
            data['file'] = b64encode(data['file']).decode() # encode as b64 then convert to string
            if data == None:
                abort(404)
            return make_response(jsonify(data), 200)
        except Exception as e:
            return make_response(jsonify({'error': 'Failed to get image', 'details': str(e)}), 500)

    @app.route('/api/v1.0/image/<id>.jpg', methods=['GET'])
    def get_image_raw(id):
        """
        Retrieve an image by its ID

        Return only the file itself
        """
        try:
            data = db.select_image(id)
            if data == None:
                abort(404)

            return send_file(BytesIO(data['file']), attachment_filename=f'{id}.jpg')
        except Exception as e:
            return make_response(jsonify({'error': 'Failed to get image', 'details': str(e)}), 500)

    @app.route('/api/v1.0/gallery/create', methods=['POST'])
    def create_gallery():
        """
        Create an image gallery

        Request body must be json:

        {
          title: ... (OPTIONAL),
          images: ... (OPTIONAL) (an image is an image ID)
        }
        """
        if not request.json:
            abort(400) # bad request
        try:
            id = db.insert_gallery(title = request.json.get('title', ''),
                                 date = datetime.now(),
                                 images = request.json.get('images', []),
                                 uploader_ip = request.remote_addr)
            return make_response(jsonify({'id': id}), 201) # created
        except Exception as e:
            return make_response(jsonify({'error': 'Failed to upload image', 'details': str(e)}), 500)

    return app
