from infra.MongoDBUtils import MyMongoClient, MyMongoCollection, MyMongoDatabase
import logging
def test_mongo_auth():
    mongo_client = MyMongoClient(log=logging.getLogger(), mongo_db_host_endpoint="mongodb://10.53.164.41", mongo_db_port=30002)
    db = mongo_client.get_existing_db(existing_db_name="tsgsdb")

    assert db.authenticate_with_db(user="tsgsuser", password="tsgspassword")

    list = db.list_all_collections_in_db()

    for item in list:
        print(item)