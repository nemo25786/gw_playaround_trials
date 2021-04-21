import datetime
from pprint import pprint
import pytest

from logic.Layer_manager_server_REST.layer_manager_utils import create_and_validate_layer, add_entities_to_layer, \
    change_entity_in_layer

layers_subset_dict = {"exists": ["607d7b22bf7ca70007ce0a79"],
                      "doesnt_exists": ["607d7b22bf7ca70007ce0a80"],
                      "empty": [],
                      }
TIME = True
BBOX = [180, 90, -180, -90]

@pytest.mark.regression
class Test_gw():
    @staticmethod
    def test_get_layers_feature_no_query(get_function_name, get_log, get_config, layer_manager_gw_client, get_status):
        layer_list = layer_manager_gw_client.get_layers_as_feature()

        for layer in layer_list:
            print(f"for layer name: {layer.name} with id: {layer.id} and entities are:")
            for entity in layer.entities:
                print(f"{layer.name}:{entity.name}:{entity.id}:{entity.updated_at}:{entity.geo_data.geometry.type}:{entity.geo_data.geometry.coordinates}")


    @pytest.mark.xfail
    @staticmethod
    def test_get_layers_feature_collection_no_query(get_function_name, get_log, get_config, layer_manager_gw_client, get_status):
        layer_list = layer_manager_gw_client.get_layers_as_feature_collection()

        for layer in layer_list:
            print(f"for layer name: {layer.name} with id: {layer.id} and entities are:")
            for entity in layer.entities:
                print(f"{layer.name}:{entity.name}:{entity.id}:{entity.updated_at}:{entity.geo_data.type}")
                for features_geo_data in entity.geo_data.features:
                    pprint(features_geo_data)





    @staticmethod
    @pytest.mark.parametrize("layers_subset_key", [("exists"),
                                                ("doesnt_exists"),
                                                ("empty")])
    def test_get_layers_feature_with_query_layers(layers_subset_key, get_function_name, get_log, get_config, layer_manager_gw_client, layer_manager_client, delete_db, get_status):
        layer_id, layer_name = create_and_validate_layer(layer_manager_client=layer_manager_client, get_log=get_log)
        layers_subset_dict["exists"] = [layer_id]
        layer_list = layer_manager_gw_client.get_layers_as_feature(layers_subset=layers_subset_dict[layers_subset_key])

        for layer in layer_list:
            print(f"for layer name: {layer.name} with id: {layer.id}")



    @staticmethod
    @pytest.mark.parametrize("layers_subset_key, since, bbox, number_of_entities", [("empty", None, [], 10),
                                                                 ("exists", None, [], 10),
                                                                 ("empty", TIME, [], 10),
                                                                 ("empty", TIME, BBOX, 10)])
    def test_get_layers_with_subset_and_bbox_and_since_query(layers_subset_key, since, bbox, number_of_entities, get_function_name, get_log, get_config, layer_manager_gw_client, layer_manager_client, delete_db, get_status):
        layer_id, layer_name = create_and_validate_layer(layer_manager_client=layer_manager_client, get_log=get_log)
        layers_subset_dict["exists"] = [layer_id]
        entities_list = add_entities_to_layer(layer_manager_client=layer_manager_client, layer_id=layer_id, get_log=get_log)

        if since is not None:
            since = datetime.datetime.utcnow().isoformat()[:-3]+'Z'

        for entity in entities_list:
            change_entity_in_layer(layer_manager_client=layer_manager_client, layer_id=layer_id, get_log=get_log, entity_id=entity.id)

        layer_list = layer_manager_gw_client.get_layers_as_feature(layers_subset=layers_subset_dict[layers_subset_key], since=since, bbox=bbox)

        assert len(layer_list[0].entities) == number_of_entities



