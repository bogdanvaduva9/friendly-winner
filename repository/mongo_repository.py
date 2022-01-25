import os

from pymongo import MongoClient


class MongoRepository:

    def __init__(self, db, collection):
        self.collection = collection
        self.db = db
        self.client = None

    def connect(self):
        self.client = MongoClient(os.environ["MONGO_STRING"])
        self.set_db()
        self.set_collection()

    def set_db(self, db=None):
        if db:
            self.db = self.client[db]
        else:
            self.db = self.client[self.db]

    def set_collection(self, collection=None):
        if collection:
            self.collection = self.db[collection]
        else:
            self.collection = self.db[self.collection]

    def add_one(self, doc):
        self.collection.insert_one(doc)

    def get_one_by_key(self, key):
        result = list(self.collection.find({"model_name": key}, {}))
        return result if not result else result[0]

    def update_one(self, doc):
        self.collection.update_one({"model_name": doc["model_name"]},
                                   {
                                       "$set": {
                                           "data": doc["data"]
                                       }
                                   })
