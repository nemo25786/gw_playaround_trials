import pymongo

class MongoCollection():
    def __init__(self, collection):
        self.collection = collection

    def create_new_doc(self, doc):
        doc = self.collection.insert_one(doc)

        return doc.inserted_id

    def delete_collection(self):
        return self.collection.drop()

    def create_multiple_docs(self, doc_list: list):
        docs = self.collection.insert_many(doc_list)

        return docs.inserted_ids

    def list_docs(self, query: dict = {}, response=None):
        found_docs = self.collection.find(query, response)

        return found_docs

    def list_all_docs(self):
        found_docs = self.collection.find({})

        return found_docs

    def delete_documents(self, query: dict = {}):
        deleted_docs = self.collection.delete_many(query)

        return deleted_docs.deleted_count

    def delete_all_documents(self):
        deleted_docs = self.collection.delete_many({})

        return deleted_docs.deleted_count

    def update_docs(self, query: dict, new_values: dict):
        updated_docs = self.collection.update_many(query, new_values)

        return updated_docs.modified_count

class MongoDatabase():
    def __init__(self, db):
        self.db = db

    def create_new_collection(self, new_collection_name: str):
        new_collection = self.db[new_collection_name]
        new_collection_object = MongoCollection(new_collection)

        return new_collection_object

    def list_all_collections_in_db(self):
        return self.db.list_collection_names()


class MongoDBException(Exception):
    pass

class MongoDBConnectionError(MongoDBException):
    pass

class MongoClient():
    def __init__(self, log, config_data):
        self.log = log
        self.config_data = config_data

        try:
            self.client = pymongo.MongoClient(config_data["SERVER"])
        except Exception as e:
            log.exception("error in connecting to MongoDB with message {}".format(str(e)))
            raise MongoDBConnectionError

    def close(self):
        self.client.close()

    def list_all_db(self):
        return self.client.list_database_names()

    def create_new_db(self, new_db_name: str):
        if new_db_name in self.client.list_database_names():
            self.log.warning("db already exists")
            return None

        new_db = self.client[new_db_name]

        new_db_object = MongoDatabase(new_db)

        return new_db_object


    def delete_db(self, db_name_for_delete):
        if db_name_for_delete not in self.client.list_database_names():
            self.log.warning("db doesn't exists")
            return None

        collection_list = self.client[db_name_for_delete].list_collection_names()
        self.client.drop_database(db_name_for_delete)

        return collection_list