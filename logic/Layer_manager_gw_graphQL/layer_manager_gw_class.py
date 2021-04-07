from pprint import pprint

from .Schema.layer_manager_gw_schema import layer_manager_gw_schema as schema, FeatureGeoData, FeatureCollectionGeoData
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

    def get_layers_as_feature(self):
        layer_gw_op = Operation(schema.Query)
        gw_layer_op = layer_gw_op.get_layers()
        self.get_all_properties_as_feature(gw_layer_op)
        query_plus_data = send_query(endpoint=self.endpoint, query=layer_gw_op, logger=self.logger)

        return query_plus_data.get_layers

    def get_layers_as_feature_collection(self):
        layer_gw_op = Operation(schema.Query)
        gw_layer_op = layer_gw_op.get_layers()
        self.get_all_properties_as_feature_collection(gw_layer_op)
        query_plus_data = send_query(endpoint=self.endpoint, query=layer_gw_op, logger=self.logger)

        return query_plus_data.get_layers

    def get_layers_and_entities(self, **kwarg):
        layer_gw_op = Operation(schema.Query)
        gw_layer_op = layer_gw_op.get_layers_and_entities(layers=kwarg.get("layers"), since=kwarg.get("since"), bbox=kwarg.get("bbox"))
        self.get_all_properties_as_feature(gw_layer_op)

        query_plus_data = send_query(endpoint=self.endpoint, query=layer_gw_op, logger=self.logger)

        return query_plus_data.get_layers_and_entities


    @staticmethod
    def get_all_properties_as_feature(gw_layer_op):
        gw_layer_op.id()
        gw_layer_op.name()
        gw_layer_op_entities = gw_layer_op.entities()
        gw_layer_op_entities.name()
        gw_layer_op_entities.type()
        gw_layer_op_entities.id()
        gw_layer_op_entities.timestamp()
        gw_layer_op_entities_geo_data_as_feature = gw_layer_op_entities.geo_data().__as__(FeatureGeoData)
        gw_layer_op_entities_geo_data_as_feature.geometry()
        gw_layer_op_entities_geo_data_as_feature.type()
        gw_layer_op_entities_geo_data_as_feature.properties()

    @staticmethod
    def get_all_properties_as_feature_collection(gw_layer_op):
        gw_layer_op.id()
        gw_layer_op.name()
        gw_layer_op_entities = gw_layer_op.entities()
        gw_layer_op_entities.name()
        gw_layer_op_entities.type()
        gw_layer_op_entities.id()
        gw_layer_op_entities.timestamp()
        gw_layer_op_entities_geo_data_as_collection = gw_layer_op_entities.geo_data().__as__(FeatureCollectionGeoData)
        gw_layer_op_entities_geo_data_as_collection.type()
        gw_layer_op_entities_geo_data_as_collection.features()