from flask import *
from datetime import datetime
from base64 import b64encode, b64decode
from io import BytesIO

from db import DB_Handler

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile("config.py")

    db = DB_Handler(app.config)

    @app.route("/")
    def page_index():
        """
        Return the static main page.

        This page allows the user to create a gallery from uploaded images.
        """
        return app.send_static_file("create.html")

    @app.route("/gallery/<id>")
    def page_gallery(id):
        """
        Return a gallery view page.
        """
        gallery = db.select_gallery(id)

        if gallery == None:
            abort(404)

        title = gallery["title"]
        date = gallery["date_created"]
        images = [db.select_image_metadata(id) for id in gallery["images"]]

        return render_template("gallery.html", title = title, date = date, images = images)


    @app.route("/api/v1.0/upload", methods=["POST"])
    def api_upload_image():
        """
        Upload an image. Request body must be json:

        {
          file: ... (REQUIED) (base64 encoded),
          description: ... (OPTIONAL)
        }
        """
        if not request.json or "file" not in request.json:
            abort(400) # bad request
        try:
            id = db.insert_image(file = b64decode(request.json["file"]),
                                 description = request.json.get("description", ""),
                                 date = datetime.now(),
                                 uploader_ip = request.remote_addr)
            return make_response(jsonify({"id": id}), 201) # created
        except Exception as e:
            return make_response(jsonify({"error": "Failed to upload image", "details": str(e)}), 500)

    @app.route("/api/v1.0/image/<id>", methods=["GET"])
    def api_get_image(id):
        """
        Retrieve an image by its ID

        Returns json response { id, file, description, upload_date }
        """
        try:
            data = db.select_image(id)
            data["file"] = b64encode(data["file"]).decode() # encode as b64 then convert to string
            if data == None:
                abort(404)
            return make_response(jsonify(data), 200)
        except Exception as e:
            return make_response(jsonify({"error": "Failed to get image", "details": str(e)}), 500)

    @app.route("/api/v1.0/image/<id>.<ext>", methods=["GET"])
    def api_get_image_raw(id, ext):
        """
        Retrieve an image by its ID

        Return only the file itself

        ext should be 'jpg' but can be anything. If it's wrong that's the browser's problem (Imgur does this, too)
        """
        try:
            data = db.select_image(id)
            if data == None:
                abort(404)

            return send_file(BytesIO(data["file"]), attachment_filename=f"{id}.{ext}")
        except Exception as e:
            return make_response(jsonify({"error": "Failed to get image", "details": str(e)}), 500)

    @app.route("/api/v1.0/gallery/create", methods=["POST"])
    def api_create_gallery():
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
            id = db.insert_gallery(title = request.json.get("title", ""),
                                 date = datetime.now(),
                                 images = request.json.get("images", []),
                                 uploader_ip = request.remote_addr)
            return make_response(jsonify({"id": id}), 201) # created
        except Exception as e:
            return make_response(jsonify({"error": "Failed to upload image", "details": str(e)}), 500)

    return app
