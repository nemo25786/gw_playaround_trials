import json
from urllib.parse import urljoin
from logging import Logger
from ccst_openapi_data_generator import OpenApiDataGenerator
from infra import RestUtils

FUNC_ptr_DICT = {
    'get': RestUtils.improved_get,
    'post': RestUtils.improved_post,
    'put': RestUtils.improved_put,
    'delete': RestUtils.improved_delete
}


class LayerManagerValidationClient(object):
    def __init__(self, endpoint: str, schema: str, log: Logger, headers: json = None, generator_config: str = None):
        if endpoint[-1] == "/":
            self.endpoint = endpoint
        else:
            self.endpoint = endpoint + "/"

        self.log = log
        self.headers = headers
        self.generator: OpenApiDataGenerator = OpenApiDataGenerator(path=schema,
                                                                    config_path=generator_config,
                                                                    generate_invalid=True,
                                                                    generate_responses=True,
                                                                    use_cache=True,
                                                                    restart_cache=False)

    def check_add_layer_valid(self):
        return self.__check_valid(endpoint="/layers", method="post")

    def check_add_layer_invalid(self):
        return self.__check_invalid(endpoint="/layers", method="post")

    def check_layer_query_valid(self):
        return self.__check_valid(endpoint="/layers/query", method="post")

    def check_layer_query_invalid(self):
        return self.__check_invalid(endpoint="/layers/query", method="post")

    def check_layer_change_valid(self):
        return self.__check_valid(endpoint="/layers/string", method="put", openapi_endpoint="/layers/{layerId}")

    def check_layer_change_invalid(self):
        return self.__check_invalid(endpoint="/layers/string", method="put", openapi_endpoint="/layers/{layerId}")

    def check_add_entity_to_layer_valid(self):
        return self.__check_valid(endpoint="/layers/string/entities", method="post", openapi_endpoint="/layers/{layerId}/entities")

    def check_add_entity_to_layer_invalid(self):
        return self.__check_invalid(endpoint="/layers/string/entities", method="post", openapi_endpoint="/layers/{layerId}/entities")

    def check_change_entity_valid(self):
        return self.__check_valid(endpoint="/layers/string/entities/string", method="put", openapi_endpoint="/layers/{layerId}/entities/{entityId}")

    def check_change_entity_invalid(self):
        return self.__check_invalid(endpoint="/layers/string/entities/string", method="put", openapi_endpoint="/layers/{layerId}/entities/{entityId}")

    def check_change_entity_invalid_all_combinations(self):
        return self.__check_invalid_all_combinations(endpoint="/layers/string/entities/string", method="put",
                                    openapi_endpoint="/layers/{layerId}/entities/{entityId}")

    def check_change_entity_valid_all_combinations(self):
        return self.__check_valid_all_combinations(endpoint="/layers/string/entities/string", method="put",
                                    openapi_endpoint="/layers/{layerId}/entities/{entityId}")

    def __check_valid(self, endpoint, method, openapi_endpoint=None):
        if openapi_endpoint is None:
            openapi_endpoint = endpoint

        request_object = self.generator.get_invalid_request_object(endpoint=openapi_endpoint, method=method)
        response = FUNC_ptr_DICT[method](url=urljoin(self.endpoint, endpoint[1:]), headers=self.headers,
                                         request_json=request_object, log=self.log)

        try:
            RestUtils.is_response_ok(response.status_code)
        except Exception as e:
            self.log.warning(f"did not receive status code ok, instead got {e}")
            return False
        else:
            return True

    def __check_valid_all_combinations(self, endpoint, method, openapi_endpoint=None):
        if openapi_endpoint is None:
            openapi_endpoint = endpoint

        request_objects = self.generator.get_all_possible_request_objects(endpoint=openapi_endpoint, method=method)

        for request_object in request_objects:
            response = FUNC_ptr_DICT[method](url=urljoin(self.endpoint, endpoint[1:]), headers=self.headers,
                                             request_json=request_object, log=self.log)

            try:
                RestUtils.is_response_ok(response.status_code)
            except Exception as e:
                self.log.warning(f"did not receive status code ok, instead got {e}")
                return False
            else:
                continue

        return True

    def __check_invalid(self, endpoint, method, openapi_endpoint=None):
        if openapi_endpoint is None:
            openapi_endpoint = endpoint

        request_object = self.generator.get_invalid_request_object(endpoint=openapi_endpoint, method=method)
        response = FUNC_ptr_DICT[method](url=urljoin(self.endpoint, endpoint[1:]), headers=self.headers,
                                         request_json=request_object, log=self.log)

        try:
            RestUtils.is_response_ok(response.status_code)
        except Exception as e:
            return True

        else:
            self.log.warning(f"did not receive status code not ok")
            return False

    def __check_invalid_all_combinations(self, endpoint, method, openapi_endpoint=None):
        if openapi_endpoint is None:
            openapi_endpoint = endpoint

        request_objects = self.generator.get_invalid_request_object(endpoint=openapi_endpoint, method=method)

        for request_object in request_objects:
            response = FUNC_ptr_DICT[method](url=urljoin(self.endpoint, endpoint[1:]), headers=self.headers,
                                         request_json=request_object, log=self.log)

            try:
                RestUtils.is_response_ok(response.status_code)
            except Exception as e:
                continue

            else:
                self.log.warning(f"did not receive status code not ok")
                return False

        return True

    # def check_add_layer_valid(self):
    #     request_object = self.generator.get_full_request_object(endpoint="/layers", method="post")
    #     response = RestUtils.improved_post(url=urljoin(self.endpoint, "/layers"), headers=self.headers,
    #                                        request_json=request_object, log=self.log)
    #
    #     try:
    #         RestUtils.is_response_ok(response.status_code)
    #     except Exception as e:
    #         self.log.warning(f"did not receive status code ok, instead got {e}")
    #         return False
    #     else:
    #         return True

    # def check_add_layer_invalid(self):
    #     request_object = self.generator.get_invalid_request_object(endpoint="/layers", method="post")
    #     response = RestUtils.improved_post(url=urljoin(self.endpoint, "/layers"), headers=self.headers,
    #                                        request_json=request_object, log=self.log)
    #
    #     try:
    #         RestUtils.is_response_ok(response.status_code)
    #     except Exception as e:
    #         return True
    #
    #     else:
    #         self.log.warning(f"did not receive status code not ok")
    #         return False


    #
    # def check_layer_query_valid(self):
    #     request_object = self.generator.get_full_request_object(endpoint="/layers/query", method="post")
    #     response = RestUtils.improved_post(url=urljoin(self.endpoint, "/layers/query"), headers=self.headers,
    #                                        request_json=request_object, log=self.log)
    #
    #     try:
    #         RestUtils.is_response_ok(response.status_code)
    #     except Exception as e:
    #         self.log.warning(f"did not receive status code ok, instead got {e}")
    #         return False
    #     else:
    #         return True

    # def check_layer_query_invalid(self):
    #     request_object = self.generator.get_invalid_request_object(endpoint="/layers/query", method="post")
    #     response = RestUtils.improved_post(url=urljoin(self.endpoint, "/layers/query"), headers=self.headers,
    #                                        request_json=request_object, log=self.log)
    #
    #     try:
    #         RestUtils.is_response_ok(response.status_code)
    #     except Exception as e:
    #         return True
    #
    #     else:
    #         self.log.warning(f"did not receive status code not ok")
    #         return False








