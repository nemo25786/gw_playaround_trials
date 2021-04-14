import json
from datetime import datetime
import pytest
from logic.Layer_manager_server_REST.layers_manager.models import Layer, Entity, LayerQuery
from faker import Faker

fake = Faker()

class Test_layers_resource(object):
    @staticmethod
    @pytest.mark.parametrize("server", [('layer_rest_server_url')])
    def test_add_layer_legal(get_function_name, get_log, get_config, server, layer_manager_client, delete_db, mongodb_client, get_status):
        date = str(datetime.utcnow().isoformat()[:-3]+'Z')
        new_layer = Layer(name=fake.unique.first_name(), created_at=date, updated_at=date)
        response = layer_manager_client.layers.post(body=new_layer, log=get_log)
        assert response is not None and response.name == new_layer.name
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response.id, log=get_log)
        assert response_get.name == response.name
        docs = mongodb_client.get_doc_by_query(query={"name": response.name})

        assert len(docs) == 1

    @staticmethod
    @pytest.mark.parametrize("server", [('layer_rest_server_url')])
    def test_add_layer_already_exists(get_function_name, get_log, get_config, server, layer_manager_client, delete_db, mongodb_client, get_status):
        date = str(datetime.utcnow().isoformat()[:-3] + 'Z')
        new_layer = Layer(name=fake.unique.first_name(), created_at=date, updated_at=date)
        response = layer_manager_client.layers.post(body=new_layer, log=get_log)
        assert response is not None and response.name == new_layer.name
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response.id, log=get_log)
        assert response_get.name == response.name
        response = layer_manager_client.layers.post(body=new_layer, log=get_log)
        assert response is None
        docs = mongodb_client.get_doc_by_query(query={"name": new_layer.name})

        assert len(docs) == 1

    @staticmethod
    @pytest.mark.parametrize("server", [('layer_rest_server_url')])
    def test_change_layer(get_function_name, get_log, get_config, server, layer_manager_client, delete_db, mongodb_client, get_status):
        date = str(datetime.utcnow().isoformat()[:-3] + 'Z')
        new_layer = Layer(name=fake.unique.first_name(), created_at=date, updated_at=date)
        response = layer_manager_client.layers.post(body=new_layer, log=get_log)
        assert response is not None and response.name == new_layer.name
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response.id, log=get_log)
        assert response_get.name == response.name
        new_layer = Layer(name=fake.unique.first_name(), created_at=date, updated_at=date)
        response = layer_manager_client.layers.layer_id_put(layer_id=response.id, body=new_layer, log=get_log)
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response.id, log=get_log)
        assert response is not None and response_get.name == new_layer.name and response_get.updated_at != date
        docs = mongodb_client.get_doc_by_query(query={"name": new_layer.name})

        assert len(docs) == 1 and docs[0]["name"] == new_layer.name and docs[0]["updatedAt"] != date

    @staticmethod
    @pytest.mark.parametrize("server", [('layer_rest_server_url')])
    def test_change_layer_doesnt_exists(get_function_name, get_log, get_config, server, layer_manager_client, delete_db, mongodb_client, get_status):
        date = str(datetime.utcnow().isoformat()[:-3] + 'Z')
        new_layer = Layer(name=fake.unique.first_name(), created_at=date, updated_at=date)
        response = layer_manager_client.layers.post(body=new_layer, log=get_log)
        assert response is not None and response.name == new_layer.name
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response.id, log=get_log)
        assert response_get.name == response.name
        response_delete = layer_manager_client.layers.layer_id_delete(layer_id=response.id)
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response.id, log=get_log)
        assert f"{response.id} does not exist" in response_get.message
        new_layer = Layer(name=fake.unique.first_name(), created_at=date, updated_at=date)
        response_put = layer_manager_client.layers.layer_id_put(layer_id=response.id, body=new_layer, log=get_log)
        assert f"{response.id} does not exist" in response_put.message

        docs = mongodb_client.get_doc_by_query(query={"name": response.name})
        assert len(docs) == 0


    @staticmethod
    @pytest.mark.parametrize("server", [('layer_rest_server_url')])
    def test_delete_layer(get_function_name, get_log, get_config, server, layer_manager_client, delete_db, mongodb_client, get_status):
        date = str(datetime.utcnow().isoformat()[:-3] + 'Z')
        new_layer = Layer(name=fake.unique.first_name(), created_at=date, updated_at=date)
        response = layer_manager_client.layers.post(body=new_layer, log=get_log)
        assert response is not None and response.name == new_layer.name
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response.id, log=get_log)
        assert response_get.name == response.name
        response_delete = layer_manager_client.layers.layer_id_delete(layer_id=response.id)
        assert response_delete is not None and response_delete.id == response.id
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response.id, log=get_log)
        assert f"{response.id} does not exist" in response_get.message
        response_delete = layer_manager_client.layers.layer_id_delete(layer_id=response.id)
        assert f"{response.id} does not exist" in response_delete.message

        docs = mongodb_client.get_doc_by_query(query={"name": response.name})
        assert len(docs) == 0

    @staticmethod
    @pytest.mark.parametrize("server", [('layer_rest_server_url')])
    def test_query_layer(get_function_name, get_log, get_config, server, layer_manager_client, delete_db, mongodb_client, get_status):
        date = str(datetime.now().isoformat()[:-3] + 'Z')
        new_layer = Layer(name=fake.unique.first_name(), created_at=date, updated_at=date)
        response_post = layer_manager_client.layers.post(body=new_layer, log=get_log)
        assert response_post is not None and response_post.name == new_layer.name
        response_get = layer_manager_client.layers.layer_id_get(layer_id=response_post.id, log=get_log)
        assert response_get.name == response_post.name

        since = str(datetime.utcnow().isoformat()[:-3] + 'Z')
        bbox = None
        layers_subset = []
        query = LayerQuery(layers=layers_subset, bbox=bbox, since=since)
        query_response = layer_manager_client.layers.query_post(body=query, log=get_log)
        assert "should NOT have fewer than 1 items" in query_response.message

        layers_subset = [response_post.id]
        query = LayerQuery(layers=layers_subset, bbox=bbox, since=since)
        query_response = layer_manager_client.layers.query_post(body=query, log=get_log)
        assert len(query_response) == 0 and query_response[0].id == response_post.id


class Test_layer_resource(object):
    @pytest.mark.parametrize("server", [('layer_rest_server_url')])
    def test_add_entity_to_layer(get_function_name, get_log, get_config, server, layer_manager_client, delete_db, get_status):
        new_entity = Entity(name=None, id=None, type=None)
        layer_manager_client.layers.layer_id_entities_entity_id_get(layer_id=None, entity_id=None)









