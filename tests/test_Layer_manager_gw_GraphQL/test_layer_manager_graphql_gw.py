import datetime
from pprint import pprint
import pytest
from logic.Layer_manager_gw_graphQL import LayerManagerGWClient
from sgqlc.types.datetime import DateTime


@pytest.mark.regression
@pytest.mark.parametrize("server", [('layer_server_url')])
def test_get_layers_feature(get_function_name, get_log, get_config, server, check_connect_to_server, get_status):
    layer_manager = LayerManagerGWClient(url=get_config["SERVICES"][server], logger=get_log, headers=None)

    layer_list = layer_manager.get_layers_as_feature()

    for layer in layer_list:
        print(f"for layer name: {layer.name} with id: {layer.id} and entities are:")
        for entity in layer.entities:
            print(f"{layer.name}:{entity.name}:{entity.id}:{entity.timestamp}:{entity.geo_data.geometry.type}:{entity.geo_data.geometry.coordinates}")


@pytest.mark.regression
@pytest.mark.parametrize("server", [('layer_server_url')])
def test_get_layers_collection(get_function_name, get_log, get_config, server, check_connect_to_server, get_status):
    layer_manager = LayerManagerGWClient(url=get_config["SERVICES"][server], logger=get_log, headers=None)

    layer_list = layer_manager.get_layers_as_feature_collection()

    for layer in layer_list:
        print(f"for layer name: {layer.name} with id: {layer.id} and entities are:")
        for entity in layer.entities:
            print(f"{layer.name}:{entity.name}:{entity.id}:{entity.timestamp}:{entity.geo_data.type}")
            for features_geo_data in entity.geo_data.features:
                pprint(features_geo_data)



TIME = DateTime(datetime.datetime.now())
BBOX = [1.3]

@pytest.mark.regression
@pytest.mark.parametrize("server, layers, since, bbox", [('layer_server_url', [], None, []),
                                                         ('layer_server_url', "1", None, []),
                                                         ('layer_server_url', [], TIME, []),
                                                         ('layer_server_url', [], None, BBOX)])
def test_get_layers_and_entities(get_function_name, get_log, get_config, server, check_connect_to_server, get_status, layers, since, bbox):
    layer_manager = LayerManagerGWClient(url=get_config["SERVICES"][server], logger=get_log, headers=None)

    layer_list = layer_manager.get_layers_and_entities(layers=layers, since=since, bbox=bbox)

    for layer in layer_list:
        print(f"for layer name: {layer.name} with id: {layer.id} and entities are:")
        for entity in layer.entities:
            print(f"{layer.name}:{entity.name}:{entity.id}:{entity.timestamp}:{entity.geo_data.geometry.type}:{entity.geo_data.geometry.coordinates}")