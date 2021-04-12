import os
from os.path import join

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
OPENAPI_CONFIG_PATH = join(ROOT_PATH, "ccst_openapi_data_generator/config/config.ini")
OPENAPI_SCHEMA = join(ROOT_PATH, "logic/Layer_manager_server_REST/OpenAPI/schema.yaml")