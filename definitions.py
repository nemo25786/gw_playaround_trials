import os
from os.path import join

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_FOLDER = join(ROOT_PATH, "config")
CONFIG_FILE = join(CONFIG_FOLDER, "config.json")
EXTERNAL_CONFIG_FILE = join(CONFIG_FOLDER, "external_config.json")
OPENAPI_CONFIG_PATH = join(ROOT_PATH, "ccst_openapi_data_generator/config/config.ini")
OPENAPI_SCHEMA = join(ROOT_PATH, "logic/Layer_manager_server_REST/OpenAPI/schema.yaml")