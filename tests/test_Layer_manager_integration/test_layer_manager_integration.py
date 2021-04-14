import pytest


@pytest.mark.integration
@pytest.mark.parametrize("server", ["layer_rest_server_url"])
class Test_layer_manager():
    @staticmethod
    def test_create_layer(get_function_name, get_log, get_config, server, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        create_layer
    @staticmethod
    def test_read_layer(get_function_name, get_log, get_config, server, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        pass
    @staticmethod
    def test_update_layer(get_function_name, get_log, get_config, server, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        pass
    @staticmethod
    def test_delete_layer(get_function_name, get_log, get_config, server, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        pass
