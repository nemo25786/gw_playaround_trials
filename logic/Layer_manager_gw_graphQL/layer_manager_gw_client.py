from pprint import pprint

from .Schema.layer_manager_gw_schema import layer_manager_gw_schema as schema, FeatureGeoData, FeatureCollectionGeoData, \
    Layer
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation
from infra.graphQLutils import *
from logging import Logger

# endpoint = HTTPEndpoint('https://api.github.com/graphql', {
#     'Authorization': 'bearer ' + os.environ['GH_TOKEN'],
# })

class LayerManagerGWClient():
    def __init__(self, url: str = None, logger: Logger = None, headers=None):
        if headers is None:
            headers = {}
        self.endpoint = HTTPEndpoint(url=url, base_headers=headers)
        self.logger = logger

    def get_layers_as_feature(self, layers_subset=[], bbox=[], since=None) -> [Layer]:
        layer_gw_op = Operation(schema.Query)
        gw_layer_op = layer_gw_op.get_layers(layer_ids=layers_subset) if len(layers_subset) else layer_gw_op.get_layers()
        self.get_all_properties_as_feature(gw_layer_op, bbox=bbox, since=since)
        query_plus_data = send_query(endpoint=self.endpoint, query=layer_gw_op, logger=self.logger)

        return query_plus_data.get_layers

    def get_layers_as_feature_collection(self, layers_subset=[], bbox=[], since=None) -> [Layer]:
        layer_gw_op = Operation(schema.Query)
        gw_layer_op = layer_gw_op.get_layers(layer_ids=layers_subset)
        self.get_all_properties_as_feature_collection(gw_layer_op, bbox=bbox, since=since)
        query_plus_data = send_query(endpoint=self.endpoint, query=layer_gw_op, logger=self.logger)

        return query_plus_data.get_layers


    @staticmethod
    def get_all_properties_as_feature(gw_layer_op, bbox, since):
        gw_layer_op.id()
        gw_layer_op.name()
        gw_layer_op_entities = choose_populate_query(gw_layer_op, bbox, since)
        gw_layer_op_entities.name()
        gw_layer_op_entities.type()
        gw_layer_op_entities.id()
        gw_layer_op_entities.updated_at()
        gw_layer_op_entities_geo_data_as_feature = gw_layer_op_entities.geo_data().__as__(FeatureGeoData)
        gw_layer_op_entities_geo_data_as_feature.geometry()
        gw_layer_op_entities_geo_data_as_feature.type()
        gw_layer_op_entities_geo_data_as_feature.properties()

    @staticmethod
    def get_all_properties_as_feature_collection(gw_layer_op, bbox, since):
        gw_layer_op.id()
        gw_layer_op.name()
        gw_layer_op_entities = choose_populate_query(gw_layer_op, bbox, since)
        gw_layer_op_entities.name()
        gw_layer_op_entities.type()
        gw_layer_op_entities.id()
        gw_layer_op_entities.updated_at()
        gw_layer_op_entities_geo_data_as_collection = gw_layer_op_entities.geo_data().__as__(FeatureCollectionGeoData)
        gw_layer_op_entities_geo_data_as_collection.type()
        gw_layer_op_entities_geo_data_as_collection.features()

def choose_populate_query(gw_layer_op, bbox, since):
    if len(bbox) and since:
        gw_layer_op_entities = gw_layer_op.entities(bbox=bbox, since=since)
    if not len(bbox) and since:
        gw_layer_op_entities = gw_layer_op.entities(since=since)
    if len(bbox) and not since:
        gw_layer_op_entities = gw_layer_op.entities(bbox=since)
    if not len(bbox) and not since:
        gw_layer_op_entities = gw_layer_op.entities()
    return gw_layer_op_entities

# def activate_function_on_webelement(driver, logger, function_name, webelement, **kwargs):
#     args = ','.join(kwargs.values())
#     try:
#         response = driver.execute_script("""return arguments[0].{}(arguments[1]);""".format(function_name),
#                                         webelement, args)
#     except Exception as e:
#         logger.error("error in executing js script with msg: {}".format(e))
#         raise e
#     return response

