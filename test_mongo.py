from bson import ObjectId

from infra.MongoDBUtils import MyMongoClient, MyMongoCollection, MyMongoDatabase
import logging

from logic.Layer_manager_server_REST.layers_manager import LayersManager


def test_mongo_auth():
    mongo_client = MyMongoClient(log=logging.getLogger(), mongo_db_host_endpoint="mongodb://10.53.164.41", mongo_db_port=30002)
    db = mongo_client.get_existing_db(existing_db_name="tsgsdb")

    assert db.authenticate_with_db(user="tsgsuser", password="tsgspassword")

    list = db.list_all_collections_in_db()

    for item in list:
        print(item)

    layer = db.get_existing_collection("layers")

    docs = layer.list_all_docs()

    for doc in docs:
        print(doc)

    layer = db.get_existing_collection("entities")

    docs = layer.list_all_docs()

    i = 0
    for doc in docs:
        i += 1
        print(doc)

    print("^ "*50, i)


def test_clear_all_db():
    mongo_client = MyMongoClient(log=logging.getLogger(), mongo_db_host_endpoint="mongodb://10.53.164.41", mongo_db_port=30002)
    db = mongo_client.get_existing_db(existing_db_name="tsgsdb")

    layer_manager_client = LayersManager(base_url="http://10.53.164.41:31156/api/v1")

    assert db.authenticate_with_db(user="tsgsuser", password="tsgspassword")

    list = db.list_all_collections_in_db()

    for item in list:
        print(item)

    entities = db.get_existing_collection("entities")

    docs = entities.list_all_docs()

    for doc in docs:
        entity_id = str(doc["_id"])
        layer_id = str(doc["layerId"])

        layer_manager_client.layers.layer_id_entities_entity_id_delete(layer_id=layer_id, entity_id=entity_id)


    docs = entities.list_all_docs()

    for doc in docs:
        entity_id = str(doc["_id"])
        layer_id = str(doc["layerId"])

        print(entity_id, layer_id)




