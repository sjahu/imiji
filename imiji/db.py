from pymongo import MongoClient
from gridfs import GridFS
import utils

class DB_Handler:
    """
    DB_Handler mediates communication between the Flask app and the MongoDB database.
    """

    def __init__(self, config):
        """
        Create a MongoDB connection.

        config - the Flask config
        """
        assert("MONGO_URI" in config) # the full URI of the MongoDB database
        assert("ID_SIZE" in config) # the number of chars to use for IDs

        self.id_size = config["ID_SIZE"]
        self.client = MongoClient(config["MONGO_URI"])
        self.db = self.client.get_default_database() # get db specified in uri
        self.images = self.db["images"] # get images collection
        self.galleries = self.db["galleries"] # get images collection
        self.fs = GridFS(self.db)

    def insert_image(self, file, description, date, uploader_ip):
        """
        Insert an image document and return the id

        file should be bytes
        """
        doc = { "id": self.gen_unique_id(), # note this is different from Mongo"s _id field
                "file": self.fs.put(file),
                "description": description,
                "date_created": date,
                "uploader_ip": uploader_ip }
        self.images.insert_one(doc)
        return doc["id"]

    def gen_unique_id(self):
        """
        Generate a unique alphanumeric id for the image

        The length of the id is controlled by self.id_size, set during class init by ID_SIZE config property.
        """
        for _ in range(5):
            id = utils.random_id(self.id_size)
            if self.images.find_one({ "id": id }) == None and \
               self.galleries.find_one({ "id": id }) == None:
                return id
        raise Exception("Failed to generate unique ID!")

    def select_image(self, id):
        """
        Select and return an image: { id, file, description, date_created }

        file is returned as bytes
        """
        doc = self.images.find_one({ "id": id })
        if doc == None:
            return None
        file = self.fs.get(doc["file"]).read()
        return { "id": id,
                 "file": file,
                 "description": doc["description"],
                 "date_created": doc["date_created"] }

    def select_image_metadata(self, id):
        """
        Select and return an image's metadata: { id, description, date_created }

        save transfering the file from the db when we don't need it
        """
        doc = self.images.find_one({ "id": id }, { "id": True, "description": True, "date_created": True })
        if doc == None:
            return None
        return { "id": id,
                 "description": doc["description"],
                 "date_created": doc["date_created"] }

    def insert_gallery(self, title, date, images, uploader_ip):
        """
        Insert a gallery document and return the id

        images is a list of image IDs
        """
        doc = { "id": self.gen_unique_id(),
                "title": title,
                "date_created": date,
                "images": images,
                "uploader_ip": uploader_ip }
        self.galleries.insert_one(doc)
        return doc["id"]

    def select_gallery(self, id):
        """
        Select and return a gallery: { id, title, date_created, images }

        images is a list of image IDs
        """
        doc = self.galleries.find_one({ "id": id })
        if doc == None:
            return None
        return { "id": id,
                 "title": doc["title"],
                 "date_created": doc["date_created"],
                 "images": doc["images"] }
