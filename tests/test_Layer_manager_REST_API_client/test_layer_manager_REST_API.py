import json
import time
from datetime import datetime, timedelta
import pytest
from logic.Layer_manager_server_REST.layers_manager.models import LayerRequest, EntityRequest, LayerQueryRequest, \
    Feature, LineString, Point
from faker import Faker

fake = Faker()

class Test_layers_resource(object):
    @staticmethod
    def test_add_layer_legal(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, get_status):
        new_layer = LayerRequest(name=fake.unique.first_name())
        response = layer_manager_client.layers.post(body=new_layer, log=get_log)
        assert response is not None and response.name == new_layer.name, get_log.error("cannot add layer")
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response.id, log=get_log)
        assert response_get.name == response.name, get_log.error("cannot get layer after creation")
        docs = mongodb_client.get_doc_by_query(query={"name": response.name})

        assert len(docs) == 1

    @staticmethod
    def test_add_layer_already_exists(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, get_status):
        new_layer = LayerRequest(name=fake.unique.first_name())
        response = layer_manager_client.layers.post(body=new_layer, log=get_log)
        assert response is not None and response.name == new_layer.name, get_log.error("cannot add layer")
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response.id, log=get_log)
        assert response_get.name == response.name, get_log.error("cannot get layer after creation")
        response = layer_manager_client.layers.post(body=new_layer, log=get_log)
        assert response is None, get_log.error("duplicate layer add allowed")
        docs = mongodb_client.get_doc_by_query(query={"name": new_layer.name})

        assert len(docs) == 1, get_log.error("cannot validate creation in Mongo")

    @staticmethod
    def test_change_layer(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, get_status):
        date = str(datetime.now().isoformat()[:-3] + 'Z')
        new_layer = LayerRequest(name=fake.unique.first_name())
        response = layer_manager_client.layers.post(body=new_layer, log=get_log)
        assert response is not None and response.name == new_layer.name, get_log.error("cannot add layer")
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response.id, log=get_log)
        assert response_get.name == response.name, get_log.error("cannot get layer after creation")
        new_layer = LayerRequest(name=fake.unique.first_name())
        response = layer_manager_client.layers.layer_id_put(layer_id=response.id, body=new_layer, log=get_log)
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response.id, log=get_log)
        assert response is not None and response_get.name == new_layer.name and response_get.updated_at != date, get_log.error("cannot update layer after creation")
        docs = mongodb_client.get_doc_by_query(query={"name": new_layer.name})

        assert len(docs) == 1 and docs[0]["name"] == new_layer.name and docs[0]["updatedAt"] != date and docs[0]["updatedAt"] != docs[0]["createdAt"], get_log.error("cannot validate layer details in Mongo")

    @staticmethod
    def test_change_layer_doesnt_exists(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, get_status):
        new_layer = LayerRequest(name=fake.unique.first_name())
        response = layer_manager_client.layers.post(body=new_layer, log=get_log)
        assert response is not None and response.name == new_layer.name, get_log.error("cannot add layer")
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response.id, log=get_log)
        assert response_get.name == response.name, get_log.error("cannot get layer after creation")
        response_delete = layer_manager_client.layers.layer_id_delete(layer_id=response.id)
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response.id, log=get_log)
        assert f"{response.id} does not exist" in response_get.message, get_log.error("invalid get of nonexisting layer allowed")
        new_layer = LayerRequest(name=fake.unique.first_name())
        response_put = layer_manager_client.layers.layer_id_put(layer_id=response.id, body=new_layer, log=get_log)
        assert f"{response.id} does not exist" in response_put.message, get_log.error(("invalid put of nonexisting layer allowed"))

        docs = mongodb_client.get_doc_by_query(query={"name": response.name})
        assert len(docs) == 0, get_log.error("cannot validate layer data in Mongo")


    @staticmethod
    def test_delete_layer(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, get_status):
        date = str(datetime.utcnow().isoformat()[:-3] + 'Z')
        new_layer = LayerRequest(name=fake.unique.first_name(), created_at=date, updated_at=date)
        response = layer_manager_client.layers.post(body=new_layer, log=get_log)
        assert response is not None and response.name == new_layer.name, get_log.error("cannot add layer")
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response.id, log=get_log)
        assert response_get.name == response.name, get_log.error("cannot get existing layer")
        response_delete = layer_manager_client.layers.layer_id_delete(layer_id=response.id)
        assert response_delete is not None and response_delete.id == response.id, get_log.error("cannot delete existing layer")
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response.id, log=get_log)
        assert f"{response.id} does not exist" in response_get.message, get_log.error("invalid get layer after delete")
        response_delete = layer_manager_client.layers.layer_id_delete(layer_id=response.id)
        assert f"{response.id} does not exist" in response_delete.message, get_log.error("invalid delete on deleted layer")

        docs = mongodb_client.get_doc_by_query(query={"name": response.name})
        assert len(docs) == 0, get_log.error("unable to validate delete in db")

    @staticmethod
    def test_query_layer(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, get_status):
        date = str(datetime.now().isoformat()[:-3] + 'Z')
        new_layer = LayerRequest(name=fake.unique.first_name(), created_at=date, updated_at=date)
        response_post = layer_manager_client.layers.post(body=new_layer, log=get_log)
        assert response_post is not None and response_post.name == new_layer.name, get_log.error("unable to add layer")
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response_post.id, log=get_log)
        assert response_get.name == response_post.name, get_log.error("unable to get existing layer")

        since = str(datetime.now().isoformat()[:-3] + 'Z')
        bbox = None
        layers_subset = []
        query = LayerQueryRequest(layers=layers_subset, bbox=bbox, since=since)
        query_response = layer_manager_client.layers.query_post(body=query, log=get_log)
        assert "should NOT have fewer than 1 items" in query_response.message, get_log.error("invalid query with missing layer subset")

        since = str(datetime.now().isoformat()[:-3] + 'Z')
        layers_subset = [response_post.id]
        query = LayerQueryRequest(layers=layers_subset, bbox=bbox, since=since)
        query_response = layer_manager_client.layers.query_post(body=query, log=get_log)
        assert len(query_response) == 1 and query_response[0].id == response_post.id, get_log.error("invalid result for query single layer")

        since = str((datetime.now()+ timedelta(seconds=100)).isoformat()[:-3] + 'Z')
        change_layer = LayerRequest(name="foooo")
        response_put = layer_manager_client.layers.layer_id_put(layer_id=response_post.id, body=change_layer)
        assert response_put is not None and response_put.name == change_layer.name, get_log.error("cannot update layer")
        query = LayerQueryRequest(layers=layers_subset, bbox=bbox, since=since)
        assert len(query_response) == 1, get_log.error("invalid result for query single layer")


class Test_entity_resource(object):
    @staticmethod
    def test_add_entity_to_layer(get_function_name, get_log, get_config, layer_manager_client, delete_db, get_status):
        new_layer = LayerRequest(name=fake.unique.first_name())
        response_post = layer_manager_client.layers.post(body=new_layer, log=get_log)
        assert response_post is not None and response_post.name == new_layer.name, get_log.error("cannot add layer")
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response_post.id, log=get_log)
        assert response_get.name == response_post.name, get_log.error("cannot get layer")

        new_entity = EntityRequest(layer_id=response_post.id, name="trial_entity", type="trial", geo_data=Feature(geometry=Point(coordinates=[1.3, 2]), properties={"someprop": "somevalue"}))
        entity_response_post = layer_manager_client.layers.layer_id_entities_post(layer_id=response_post.id, body=[new_entity])

        assert len(entity_response_post) == 1 and entity_response_post[0].name == new_entity.name, get_log.error("cannot add entity to layer")

        new_entity = EntityRequest(layer_id=response_post.id, name="trial_entity", type="trial", geo_data=Feature(geometry=Point(coordinates=[1.3, -300]), properties={"someprop": "somevalue"}))
        entity_response_post = layer_manager_client.layers.layer_id_entities_post(layer_id=response_post.id, body=[new_entity])

        assert "longitude/latitude is out of bounds" in entity_response_post.message, get_log.error("entity with illegal coordinates allowed - longitude")

        new_entity = EntityRequest(layer_id=response_post.id, name="trial_entity", type="trial", geo_data=Feature(geometry=Point(coordinates=[100.3, -100]), properties={"someprop": "somevalue"}))
        entity_response_post = layer_manager_client.layers.layer_id_entities_post(layer_id=response_post.id, body=[new_entity])

        assert "longitude/latitude is out of bounds" in entity_response_post.message, get_log.error("entity with illegal coordinates allowed - latitue")

        new_entity = EntityRequest(layer_id=response_post.id, name="trial_entity", type="trial", geo_data=Feature(geometry=Point(coordinates=[1.3, 2]), properties={"someprop": "somevalue"}))
        entity_response_post = layer_manager_client.layers.layer_id_entities_post(layer_id=response_post.id,
                                                                                  body=[new_entity])
        assert len(entity_response_post) == 1 and entity_response_post[0].name == new_entity.name, get_log.error("duplicate entity name allowed in single add")

        new_entity = EntityRequest(layer_id=response_post.id, name="trial_entity", type="trial", geo_data=Feature(geometry=Point(coordinates=[0, 0]), properties={"someprop": "somevalue"}))
        entity_response_post = layer_manager_client.layers.layer_id_entities_post(layer_id=response_post.id, body=[new_entity, new_entity])

        assert len(entity_response_post) == 1 and entity_response_post[0].name == new_entity.name, get_log.error("duplicate entity name allowed in batch add")

    @staticmethod
    def test_delete_entity_from_layer(get_function_name, get_log, get_config, layer_manager_client, delete_db, get_status):
        new_layer = LayerRequest(name=fake.unique.first_name())
        response_post = layer_manager_client.layers.post(body=new_layer, log=get_log)
        assert response_post is not None and response_post.name == new_layer.name
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response_post.id, log=get_log)
        assert response_get.name == response_post.name

        new_entity = EntityRequest(layer_id=response_post.id, name="trial_entity", type="trial", geo_data=Feature(geometry=Point(coordinates=[1.3, 2]), properties={"someprop": "somevalue"}))
        entity_response_post = layer_manager_client.layers.layer_id_entities_post(layer_id="fooo", body=[new_entity])


        entity_response_post = layer_manager_client.layers.layer_id_entities_post(layer_id=response_post.id, body=[new_entity])

        assert len(entity_response_post) == 1 and entity_response_post[0].name == new_entity.name

        new_entity2 = EntityRequest(layer_id=response_post.id, name="trial_entity_2", type="trial", geo_data=Feature(geometry=Point(coordinates=[1.3, 2]), properties={"someprop": "somevalue"}))
        entity2_response_post = layer_manager_client.layers.layer_id_entities_post(layer_id=response_post.id, body=[new_entity2])

        assert len(entity2_response_post) == 1 and entity2_response_post[0].name == new_entity2.name

        delete_entity_response = layer_manager_client.layers.layer_id_entities_entity_id_delete(layer_id=response_post.id, entity_id=entity_response_post[0].id)

        assert delete_entity_response.name == new_entity.name

        get_entity_response = layer_manager_client.layers.layer_id_entities_entity_id_get(layer_id=response_post.id, entity_id=entity_response_post[0].id)

        assert f"Entity id: {entity_response_post[0].id} does not exist" in get_entity_response.message

        very_new_entity = EntityRequest(layer_id=response_post.id, name="trial_entity", type="trial", geo_data=Feature(geometry=Point(coordinates=[1.3, 2]), properties={"someprop": "somevalue"}))
        new_entity_response_post = layer_manager_client.layers.layer_id_entities_post(layer_id=response_post.id, body=[very_new_entity])

        assert len(new_entity_response_post) == 1 and new_entity_response_post[0].created_at != entity_response_post[0].created_at

        entity2_response_get = layer_manager_client.layers.layer_id_entities_entity_id_get(layer_id=response_post.id, entity_id=entity2_response_post[0].id)

        assert entity2_response_get.name == entity2_response_post[0].name

    @staticmethod
    def test_update_entity_in_layer(get_function_name, get_log, get_config, layer_manager_client, delete_db, get_status):
        new_layer = LayerRequest(name=fake.unique.first_name())
        response_post = layer_manager_client.layers.post(body=new_layer, log=get_log)
        assert response_post is not None and response_post.name == new_layer.name
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response_post.id, log=get_log)
        assert response_get.name == response_post.name

        new_entity = EntityRequest(layer_id=response_post.id, name="trial_entity", type="trial", geo_data=Feature(geometry=Point(coordinates=[1.3, 2]), properties={"someprop": "somevalue"}))
        entity_response_post = layer_manager_client.layers.layer_id_entities_post(layer_id=response_post.id, body=[new_entity])

        assert len(entity_response_post) == 1 and entity_response_post[0].name == new_entity.name

        changed_entity = EntityRequest(layer_id=response_post.id, name="changed_trial_entity", type="trial", geo_data=Feature(geometry=Point(coordinates=[0, -2]), properties={"someprop": "someothervalue"}))
        changed_entity_put_response = layer_manager_client.layers.layer_id_entities_entity_id_put(layer_id=response_post.id, entity_id=entity_response_post[0].id, body=changed_entity)

        assert changed_entity_put_response.name == changed_entity.name and changed_entity_put_response.id == entity_response_post[0].id

        changed_entity_get_response = layer_manager_client.layers.layer_id_entities_entity_id_get(layer_id=response_post.id, entity_id=entity_response_post[0].id)

        assert changed_entity_get_response.name == changed_entity.name

        entity_delete_response =layer_manager_client.layers.layer_id_entities_entity_id_delete(layer_id=response_post.id, entity_id=entity_response_post[0].id)

        assert entity_delete_response.name == changed_entity.name

        invalid_changed_entity_get_response = layer_manager_client.layers.layer_id_entities_entity_id_get(layer_id=response_post.id, entity_id=entity_response_post[0].id)

        assert "does not exist" in invalid_changed_entity_get_response.message


























