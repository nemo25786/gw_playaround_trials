import random

from faker import Faker
from logging import Logger, getLogger

from logic.Layer_manager_server_REST.layers_manager import LayersManager
from logic.Layer_manager_server_REST.layers_manager.models import LayerRequest, LayerQueryRequest, EntityRequest, Point, \
    Feature

fake = Faker()

LAYER_NAME = "vehicles"

def generate_random_entity_body(layer_id, geojson_type=Point) ->EntityRequest:
    entity_body = EntityRequest(layer_id=layer_id,
                                name=fake.unique.first_name(),
                                external_id=random.randint(0, 250),
                                type="plane",
                                geo_data=Feature(geometry=geojson_type(
                                coordinates=[random.uniform(-180, 180), random.uniform(-90, 90)]),
                                properties={"heading": random.uniform(0, 360)}))

    return entity_body


def generate_random_layer_body(name=fake.unique.first_name()) -> LayerRequest:
    layer_body = LayerRequest(name=name)

    return layer_body


def create_and_validate_layer(layer_manager_client: LayersManager, get_log: Logger, layer_body: LayerRequest=generate_random_layer_body()) -> tuple:
    response = layer_manager_client.layers.post(body=layer_body, log=get_log)
    assert response.name == layer_body.name, get_log.error("unable to add new layer")
    response_get = layer_manager_client.layers.layer_id_get(layer_id=response.id, log=get_log)
    assert response_get.name == response.name, get_log.error("unable to get existing layer")

    return response.id, response.name

def update_layer(layer_manager_client: LayersManager, layer_id, get_log: Logger, layer_body:LayerRequest=generate_random_layer_body()) -> tuple:
    response = layer_manager_client.layers.layer_id_put(layer_id=layer_id, body=layer_body, log=get_log)

    assert response.name == layer_body.name, get_log.error("unable to update existing layer")

    return response.id, response.name

def delete_layer(layer_manager_client: LayersManager, get_log: Logger, layer_id) -> tuple:
    response = layer_manager_client.layers.layer_id_delete(layer_id=layer_id)

    assert response.id == layer_id, get_log.error("unable to delete layer")

    return response.id, response.name

def get_all_layers(layer_manager_client: LayersManager, get_log: Logger) -> list:
    layer_get_response = layer_manager_client.layers.get(log=get_log)

    assert layer_get_response is list, get_log.error("unable to get all layers")

    return layer_get_response

def query_layers_for_entities(layer_manager_client: LayersManager, get_log: Logger, layer_ids: list, since:str, bbox: [float]) -> list:
    layer_request = LayerQueryRequest(layers=layer_ids, since=since, bbox=bbox)
    layer_request_response = layer_manager_client.layers.query_post(body=layer_request, log=get_log)

    assert layer_request_response is list, get_log.error("unable to query for entities using post")

    return layer_request_response

def add_entities_to_layer(layer_manager_client: LayersManager, get_log: Logger, layer_id, entity_request_body_list=[]):
    if len(entity_request_body_list) == 0:
        entity_request_body_list = [generate_random_entity_body(layer_id=layer_id) for i in range(10)]

    post_entities_response = layer_manager_client.layers.layer_id_entities_post(layer_id=layer_id, log=get_log, body=entity_request_body_list)

    assert len(post_entities_response) == len(entity_request_body_list), get_log.error("unable to add entities to layer")

    return post_entities_response

def change_entity_in_layer(layer_manager_client: LayersManager, get_log: Logger, layer_id, entity_id, entity_request_body_change: EntityRequest=None):
    get_old_entity_response = layer_manager_client.layers.layer_id_entities_entity_id_get(layer_id=layer_id, entity_id=entity_id)

    assert get_old_entity_response.id == entity_id, get_log.error("unable to get entity for change")

    if entity_request_body_change is None:
        entity_request_body_change = generate_random_entity_body(layer_id)

    put_entity_response = layer_manager_client.layers.layer_id_entities_entity_id_put(layer_id=layer_id,
                                                                entity_id=entity_id,
                                                                body=entity_request_body_change)

    assert put_entity_response.updated_at != get_old_entity_response.updated_at, get_log.error("unable to update entitiy")

    return put_entity_response

def get_entity_in_layer(layer_manager_client: LayersManager, get_log: Logger, layer_id, entity_id):
    get_entity_response = layer_manager_client.layers.layer_id_entities_entity_id_get(layer_id=layer_id, entity_id=entity_id)

    assert get_entity_response.id == entity_id, get_log.error("unable to get entity in layer")

    return get_entity_response


