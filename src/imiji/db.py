from pymongo import MongoClient
from gridfs import GridFS
import utils
from base64 import b64encode, b64decode

class DB_Handler:
    def __init__(self, config):
        """
        Create a MongoDB connection.

        config - the Flask config
        """
        assert('MONGO_URI' in config) # the full URI of the MongoDB database
        assert('ID_SIZE' in config) # the number of chars to use for IDs

        self.id_size = config['ID_SIZE']
        self.client = MongoClient(config['MONGO_URI'])
        self.db = self.client.get_default_database() # get db specified in uri
        self.images = self.db['images'] # get images collection
        self.fs = GridFS(self.db)

    def insert_image(self, file, description, upload_date, uploader_ip):
        """
        Insert an image document and return the id
        """
        doc = { 'id': self.gen_unique_id(), # note this is different from Mongo's _id field
                'file': self.fs.put(file.encode()),
                'description': description,
                'upload_date': upload_date,
                'uploader_ip': uploader_ip
              }
        self.images.insert_one(doc)
        return doc['id']

    def gen_unique_id(self):
        for _ in range(5):
            id = utils.random_id(self.id_size)
            if self.images.find_one({ 'id': id }) == None:
                return id
        raise Exception("Failed to generate unique ID!")

    def select_image(self, id):
        """
        Select and return an image
        """
        doc = self.images.find_one({ 'id': id })
        if doc == None:
            return None
        file = b64encode(self.fs.get(doc['file']).read()).decode() # read file and convert to b64
        return { 'id': id, 'file': file, 'description': doc['description'], 'upload_date': doc['upload_date']}
