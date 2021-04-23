import json
from urllib.parse import urljoin

from definitions import CONFIG_FILE, EXTERNAL_CONFIG_FILE

internal_config_data = {
    "DEFAULT": {
        "log_folder": "logs"
    },
    "general": {
        "grafana_tag": "QA",
        "project_key": "TSIN",
        "version_id": "-1",
        "cycle_id": "-1"
    },
    "AUTH": {
        "GRAFANA_API_KEY": "eyJrIjoiV1VVWEhySFdubW9nb0xCZ2F0OWVpRE5jVkpwNndUS1giLCJuIjoidHNnc2dyYWZhbmEiLCJpZCI6MX0",
        "GRAFANA_USER": "tals",
        "GRAFANA_PASSWORD": "Tt123456!",
        "zapi_account_id": "5f7633e0e31b69006f962ed1",
        "zapi_access_key": "OTU1NTA3MTEtNDM5Yi0zYzkyLWE2ODUtMTIzNzJkNGVjMjFjIDVmNzYzM2UwZTMxYjY5MDA2Zjk2MmVkMSBVU0VSX0RFRkFVTFRfTkFNRQ",
        "zapi_secret_key": "RgcCopajky46gvRPiB1-hoSNKJBLB5X42s2nMZjYels",
        "allure_token": "75bd5d28-2748-4beb-81aa-e0514a73a147__getattribute__()",
        "mongo_db_user": "tsgsuser",
        "mongo_db_password": "tsgspassword"
    },
    "JIRA": {
        "jira_user_mail": "talsht@rafael.co.il",
        "jira_user_API_token": "i9G46cUiYS17cjX6t9Zx36B0",
        "jira_base_url": "https://rnd-hub.atlassian.net"
    },
    "SERVICES": {
        "grafana_server_external": "10.53.164.41",
        "grafana_server_internal": "pro-grafana.monitoring",
        "grafana_external_port": "32300",
        "grafana_internal_port": "80",
        "layer_manager_gw_url": "http://10.53.164.41:31155/graphql",
        "layer_manager_gw_livenss": "http://10.53.164.41:31155/.well-known/apollo/server-health/",
        "allure_report_address": "http://allure-ee-gateway.qa:8080",
        "layer_rest_server_url": "http://10.53.164.41:31156/api/v1",
        "layer_manager_server_livenss": "http://10.53.164.41:31156/liveness",
        "layer_manager_mongo_db_port": "30002",
        "layer_manager_mongo_db": "mongodb://10.53.164.41",
        "mongo_layers_db": "tsgsdb",
        "mongo_layers_collection": "layers",
        "mongo_aircrafts_collection": "entities"
    }
}
external_config_data = {
    "DEFAULT": {
        "log_folder": "logs"
    },
    "general": {
        "grafana_tag": "QA",
        "project_key": "TSIN",
        "version_id": "-1",
        "cycle_id": "-1"
    },
    "AUTH": {
        "GRAFANA_API_KEY": "eyJrIjoiV1VVWEhySFdubW9nb0xCZ2F0OWVpRE5jVkpwNndUS1giLCJuIjoidHNnc2dyYWZhbmEiLCJpZCI6MX0",
        "GRAFANA_USER": "tals",
        "GRAFANA_PASSWORD": "Tt123456!",
        "zapi_account_id": "5f7633e0e31b69006f962ed1",
        "zapi_access_key": "OTU1NTA3MTEtNDM5Yi0zYzkyLWE2ODUtMTIzNzJkNGVjMjFjIDVmNzYzM2UwZTMxYjY5MDA2Zjk2MmVkMSBVU0VSX0RFRkFVTFRfTkFNRQ",
        "zapi_secret_key": "RgcCopajky46gvRPiB1-hoSNKJBLB5X42s2nMZjYels",
        "allure_token": "75bd5d28-2748-4beb-81aa-e0514a73a147",
        "mongo_db_user": "tsgsuser",
        "mongo_db_password": "tsgspassword"
    },
    "JIRA": {
        "jira_user_mail": "talsht@rafael.co.il",
        "jira_user_API_token": "i9G46cUiYS17cjX6t9Zx36B0",
        "jira_base_url": "https://rnd-hub.atlassian.net"
    },
    "SERVICES": {
        "grafana_server_external": "10.53.164.41",
        "grafana_server_internal": "10.53.164.41",
        "grafana_external_port": "32300",
        "grafana_internal_port": "32300",
        "layer_manager_gw_url": "http://10.53.164.41:31155/graphql",
        "layer_manager_gw_livenss": "http://10.53.164.41:31155/.well-known/apollo/server-health/",
        "layer_rest_server_url": "http://localhost:3000/api/v1",
        "layer_manager_server_livenss": "http://10.53.164.41:31156/liveness",
        "allure_report_address": "http://10.53.164.41:31969",
        "layer_server_url": "http://localhost:3005",
        "layer_manager_mongo_db_port": "30002",
        "layer_manager_mongo_db": "mongodb://10.53.164.41",
        "mongo_db": "tsgsdb",
        "mongo_collection": "layers",
        "mongo_aircrafts_collection": "entities"
    }
}
def external_create_config():
    with open(CONFIG_FILE, mode="w", encoding="utf-8") as file:
        json.dump(internal_config_data, file)


def internal_create_config():
    with open(EXTERNAL_CONFIG_FILE, mode="w", encoding="utf-8") as file:
        json.dump(external_config_data, file)

if __name__ == "__main__":
    external_create_config()
    internal_create_config()