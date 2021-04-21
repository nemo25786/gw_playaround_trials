import math
import time

import pytest
from bson import ObjectId
from faker import Faker
import random
from logging import Logger

from logic.Layer_manager_server_REST.layer_manager_utils import create_and_validate_layer, delete_layer, update_layer
from logic.Layer_manager_server_REST.layers_manager.models import LayerRequest, LayerQueryRequest, EntityRequest, Point, \
    Feature
from infra.MongoDBUtils import MyMongoCollection
from logic.Layer_manager_gw_graphQL import LayerManagerGWClient

fake = Faker()

LAYER_NAME = "vehicles"


def validate_layer_creation_in_db(mongodb_client: MyMongoCollection, layer_id, layer_name:str, get_log: Logger):
    docs = mongodb_client.get_doc_by_query(query={"_id": ObjectId(layer_id)})
    assert len(docs) == 1 and docs[0]["name"] == layer_name, get_log.error("unable to validate layer creation in Mongo")

def validate_layer_creation_in_gw(layer_manager_gw_client:LayerManagerGWClient, layer_id, layer_name:str, get_log: Logger):
    layers = layer_manager_gw_client.get_layers_as_feature(layers_subset=[str(layer_id)])
    assert len(layers) == 1 and layers[0].name == layer_name, get_log.error("unable to validate layer creation in GW")


@pytest.mark.integration
class Test_layer_manager():
    @staticmethod
    def test_create_and_validate_layer(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        layer_id, layer_name = create_and_validate_layer(layer_manager_client, get_log)
        validate_layer_creation_in_db(mongodb_client, layer_id, layer_name, get_log)
        validate_layer_creation_in_gw(layer_manager_gw_client, layer_id, layer_name, get_log)

    @staticmethod
    def test_read_layer(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        for i in range(10):
            layer_id, layer_name = create_and_validate_layer(layer_manager_client, get_log, layer_body=LayerRequest(name=fake.unique.first_name()))
            validate_layer_creation_in_db(mongodb_client, layer_id, layer_name, get_log)
            validate_layer_creation_in_gw(layer_manager_gw_client, layer_id, layer_name, get_log)

    @staticmethod
    def test_update_layer(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        layer_id, layer_name = create_and_validate_layer(layer_manager_client, get_log, layer_body=LayerRequest(name=fake.unique.first_name()))
        validate_layer_creation_in_gw(layer_manager_gw_client, layer_id, layer_name, get_log)
        updated_layer_id, updated_layer_name = update_layer(layer_manager_client, layer_id, get_log, layer_body=LayerRequest(name=fake.unique.first_name()))
        validate_layer_creation_in_db(mongodb_client, updated_layer_id, updated_layer_name, get_log)
        validate_layer_creation_in_gw(layer_manager_gw_client, layer_id, updated_layer_name, get_log)

        try:
            validate_layer_creation_in_gw(layer_manager_gw_client, layer_id, layer_name, get_log)
        except AssertionError:
            assert True
        else:
            assert False

    @staticmethod
    def test_delete_layer(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        layer_id, layer_name = create_and_validate_layer(layer_manager_client, get_log, layer_body=LayerRequest(name=fake.unique.first_name()))
        deleted_layer_id, deleted_layer_name = delete_layer(layer_manager_client, layer_id=layer_id, get_log=get_log)

        try:
            validate_layer_creation_in_db(mongodb_client, deleted_layer_id, deleted_layer_name, get_log)
        except AssertionError:
            assert True
        else:
            assert False

        try:
            validate_layer_creation_in_gw(layer_manager_gw_client, deleted_layer_id, deleted_layer_name, get_log)
        except AssertionError:
            assert True
        else:
            assert False


    @staticmethod
    def test_add_random_entities(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        new_layer = LayerRequest(name=LAYER_NAME)
        new_layer_post_response = layer_manager_client.layers.post(body=new_layer)

        assert new_layer_post_response is not None and new_layer_post_response.name == LAYER_NAME

        for i in range(10):
            new_entity_name = f"{fake.unique.first_name()}_{i}"
            new_entity = EntityRequest(layer_id=new_layer_post_response.id,
                                       name=new_entity_name,
                                       type="BMW",
                                       geo_data=Feature(geometry=Point(coordinates=[random.randint(-180, 180), random.randint(-90, 90)]),
                                                        properties={"heading": random.randint(0, 4) * 90}))
            new_entity_post_request = layer_manager_client.layers.layer_id_entities_post(layer_id=new_layer_post_response.id,
                                                                                         body=[new_entity])
            assert new_entity_post_request[0].name == new_entity_name

        while (1):
            query = LayerQueryRequest(layers=[new_layer_post_response.id])
            query_results = layer_manager_client.layers.query_post(body=query, log=get_log)

            for entity in query_results[0].entities:
                coordinates = entity.geo_data["geometry"]["coordinates"]
                heading = entity.geo_data["properties"]["heading"]

                long_factor, lat_factor = 0, 0
                sign_factor_lat = 1 if (coordinates[0]) > 0 else -1
                sign_factor_lon = 1 if (coordinates[1]) > 0 else -1

                if heading == 0:
                    long_factor = 1
                    lat_factor = 0
                if heading == 180:
                    long_factor = -1
                    lat_factor = 0
                if heading == 90:
                    lat_factor = 1
                    long_factor = 0
                if heading == 270:
                    lat_factor = -1
                    long_factor = 0

                new_coordinates = [((coordinates[0] + lat_factor * 0.1) % 180), ((coordinates[1] + long_factor * 0.1) % 90)]
                changed_entity = EntityRequest(layer_id=new_layer_post_response.id, name=entity.name, type="BMW",
                                           geo_data=Feature(geometry=Point(coordinates=new_coordinates), properties={"heading": heading}))
                put_result = layer_manager_client.layers.layer_id_entities_entity_id_put(layer_id=new_layer_post_response.id,
                                                                                         entity_id=entity.id,
                                                                                         body=changed_entity)
                assert put_result.updated_at != entity.updated_at

            time.sleep(1)





