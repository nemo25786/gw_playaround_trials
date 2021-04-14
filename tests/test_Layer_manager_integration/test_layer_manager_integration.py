import datetime

import pytest
from bson import ObjectId
from faker import Faker

from logic.Layer_manager_server_REST.layers_manager.models import Layer
from infra.MongoDBUtils import MyMongoCollection
from logic.Layer_manager_server_REST.layers_manager import LayersManager
from logic.Layer_manager_gw_graphQL_new import LayerManagerGWClient

fake = Faker()


def create_layer(layer_manager_client: LayersManager, get_log):
    date = str(datetime.datetime.now().isoformat()[:-3] + 'Z')
    new_layer = Layer(name=fake.unique.first_name(), created_at=date, updated_at=date)
    response = layer_manager_client.layers.post(body=new_layer, log=get_log)
    assert response.name == new_layer.name
    response_get = layer_manager_client.layers.layer_id_get(layer_id=response.id, log=get_log)
    assert response_get.name == response.name

    return response.id, response.name

def update_layer(layer_manager_client: LayersManager, layer_id, get_log):
    new_name = fake.unique.first_name()
    updated_layer = Layer(name=new_name)
    response = layer_manager_client.layers.layer_id_put(layer_id=layer_id, body=updated_layer, log=get_log)

    assert response.name == new_name

    return response.id, response.name

def delete_layer(layer_manager_client: LayersManager, layer_id):
    response = layer_manager_client.layers.layer_id_delete(layer_id=layer_id)

    assert response.id == layer_id

    return response.id, response.name

def validate_creation_in_db(mongodb_client: MyMongoCollection, layer_id, layer_name):
    docs = mongodb_client.get_doc_by_query(query={"_id": ObjectId(layer_id)})
    assert len(docs) == 1 and docs[0]["name"] == layer_name

def validate_creation_in_gw(layer_manager_gw_client:LayerManagerGWClient, layer_id, layer_name):
    layers = layer_manager_gw_client.get_layers_as_feature_wo_entities_with_query_param(layers_subset=[str(layer_id)])

    assert len(layers) == 1 and layers[0].name == layer_name


@pytest.mark.integration
@pytest.mark.parametrize("server", ["layer_rest_server_url"])
class Test_layer_manager():
    @staticmethod
    def test_create_layer(get_function_name, get_log, get_config, server, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        layer_id, layer_name = create_layer(layer_manager_client, get_log)
        validate_creation_in_db(mongodb_client, layer_id, layer_name)
        validate_creation_in_gw(layer_manager_gw_client, layer_id, layer_name)

    @staticmethod
    def test_read_layer(get_function_name, get_log, get_config, server, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        for i in range(10):
            layer_id, layer_name = create_layer(layer_manager_client, get_log)
            validate_creation_in_db(mongodb_client, layer_id, layer_name)
            validate_creation_in_gw(layer_manager_gw_client, layer_id, layer_name)

    @staticmethod
    def test_update_layer(get_function_name, get_log, get_config, server, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        layer_id, layer_name = create_layer(layer_manager_client, get_log)
        validate_creation_in_gw(layer_manager_gw_client, layer_id, layer_name)
        updated_layer_id, updated_layer_name = update_layer(layer_manager_client, layer_id, get_log)
        validate_creation_in_db(mongodb_client, updated_layer_id, updated_layer_name)
        validate_creation_in_gw(layer_manager_gw_client, layer_id, updated_layer_name)

        try:
            validate_creation_in_gw(layer_manager_gw_client, layer_id, layer_name)
        except AssertionError:
            assert True
        else:
            assert False

    @staticmethod
    def test_delete_layer(get_function_name, get_log, get_config, server, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        layer_id, layer_name = create_layer(layer_manager_client, get_log)
        deleted_layer_id, deleted_layer_name = delete_layer(layer_manager_client, layer_id)

        try:
            validate_creation_in_db(mongodb_client, deleted_layer_id, deleted_layer_name)
        except AssertionError:
            assert True
        else:
            assert False

        try:
            validate_creation_in_gw(layer_manager_gw_client, deleted_layer_id, deleted_layer_name)
        except AssertionError:
            assert True
        else:
            assert False




