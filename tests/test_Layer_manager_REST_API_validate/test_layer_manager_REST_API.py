from datetime import datetime
import pytest
from logic.Layer_manager_server_REST.layers_manager.models import Layer
from faker import Faker

fake = Faker()

class Test_post_layer(object):
    @staticmethod
    @pytest.mark.parametrize("server", [('layer_rest_server_url')])
    def test_add_layer_legal(get_function_name, get_log, get_config, server, layer_manager_client, delete_db, get_status):
        date = str(datetime.utcnow().isoformat()[:-3]+'Z')
        new_layer = Layer(name=fake.unique.first_name(), created_at=date, updated_at=date)
        reponse = layer_manager_client.layers.post(body=new_layer)

        assert reponse is not None and reponse.name == new_layer.name

        reponse_get = layer_manager_client.layers.layer_id_get(layer_id=reponse.id)

        assert reponse_get.name == reponse.name

    @staticmethod
    @pytest.mark.parametrize("server", [('layer_rest_server_url')])
    def test_add_layer_already_exists(get_function_name, get_log, get_config, server, layer_manager_client, delete_db, get_status):
        date = str(datetime.utcnow().isoformat()[:-3] + 'Z')
        new_layer = Layer(name=fake.unique.first_name(), created_at=date, updated_at=date)
        reponse = layer_manager_client.layers.post(body=new_layer)

        assert reponse is not None and reponse.name == new_layer.name

        reponse_get = layer_manager_client.layers.layer_id_get(layer_id=reponse.id)

        assert reponse_get.name == reponse.name

        reponse = layer_manager_client.layers.post(body=new_layer)

        assert reponse is None

    @staticmethod
    @pytest.mark.parametrize("server", [('layer_rest_server_url')])
    def test_change_layer(get_function_name, get_log, get_config, server, layer_manager_client, delete_db, get_status):
        date = str(datetime.utcnow().isoformat()[:-3] + 'Z')
        new_layer = Layer(name=fake.unique.first_name(), created_at=date, updated_at=date)
        reponse = layer_manager_client.layers.post(body=new_layer)

        assert reponse is not None and reponse.name == new_layer.name

        reponse_get = layer_manager_client.layers.layer_id_get(layer_id=reponse.id)

        assert reponse_get.name == reponse.name

        new_layer = Layer(name=fake.unique.first_name(), created_at=date, updated_at=date)
        reponse = layer_manager_client.layers.layer_id_put(layer_id=reponse.id, body=new_layer)

        reponse_get = layer_manager_client.layers.layer_id_get(layer_id=reponse.id)

        assert reponse is not None and reponse_get.name == new_layer.name and reponse_get.updated_at != date






