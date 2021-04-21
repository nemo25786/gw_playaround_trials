import sgqlc.types
import sgqlc.types.datetime


layer_manager_gw_schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean

class CacheControlScope(sgqlc.types.Enum):
    __schema__ = layer_manager_gw_schema
    __choices__ = ('PUBLIC', 'PRIVATE')


class Coordinates(sgqlc.types.Scalar):
    __schema__ = layer_manager_gw_schema


DateTime = sgqlc.types.datetime.DateTime

Float = sgqlc.types.Float

class GeoDataType(sgqlc.types.Enum):
    __schema__ = layer_manager_gw_schema
    __choices__ = ('Feature', 'FeatureCollection')


class GeometryType(sgqlc.types.Enum):
    __schema__ = layer_manager_gw_schema
    __choices__ = ('Point', 'LineString', 'Polygon', 'MultiPoint', 'MultiLineString', 'MultiPolygon')


Int = sgqlc.types.Int

class JSONObject(sgqlc.types.Scalar):
    __schema__ = layer_manager_gw_schema


String = sgqlc.types.String

class Upload(sgqlc.types.Scalar):
    __schema__ = layer_manager_gw_schema



########################################################################
# Input Objects
########################################################################

########################################################################
# Output Objects and Interfaces
########################################################################
class Entity(sgqlc.types.Type):
    __schema__ = layer_manager_gw_schema
    __field_names__ = ('id', 'name', 'type', 'updated_at', 'geo_data')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    geo_data = sgqlc.types.Field('GeoData', graphql_name='geoData')


class GeoData(sgqlc.types.Interface):
    __schema__ = layer_manager_gw_schema
    __field_names__ = ('type',)
    type = sgqlc.types.Field(sgqlc.types.non_null(GeoDataType), graphql_name='type')


class Geometry(sgqlc.types.Type):
    __schema__ = layer_manager_gw_schema
    __field_names__ = ('type', 'coordinates')
    type = sgqlc.types.Field(sgqlc.types.non_null(GeometryType), graphql_name='type')
    coordinates = sgqlc.types.Field(sgqlc.types.non_null(Coordinates), graphql_name='coordinates')


class Layer(sgqlc.types.Type):
    __schema__ = layer_manager_gw_schema
    __field_names__ = ('id', 'name', 'entities')
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    entities = sgqlc.types.Field(sgqlc.types.list_of(Entity), graphql_name='entities', args=sgqlc.types.ArgDict((
        ('since', sgqlc.types.Arg(DateTime, graphql_name='since', default=None)),
        ('bbox', sgqlc.types.Arg(sgqlc.types.list_of(Float), graphql_name='bbox', default=None)),
))
    )


class Query(sgqlc.types.Type):
    __schema__ = layer_manager_gw_schema
    __field_names__ = ('get_layers',)
    get_layers = sgqlc.types.Field(sgqlc.types.list_of(Layer), graphql_name='getLayers', args=sgqlc.types.ArgDict((
        ('layer_ids', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='layerIds', default=None)),
))
    )


class FeatureCollectionGeoData(sgqlc.types.Type, GeoData):
    __schema__ = layer_manager_gw_schema
    __field_names__ = ('features',)
    features = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('FeatureGeoData')), graphql_name='features')


class FeatureGeoData(sgqlc.types.Type, GeoData):
    __schema__ = layer_manager_gw_schema
    __field_names__ = ('geometry', 'properties')
    geometry = sgqlc.types.Field(Geometry, graphql_name='geometry')
    properties = sgqlc.types.Field(JSONObject, graphql_name='properties')



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
layer_manager_gw_schema.query_type = Query
layer_manager_gw_schema.mutation_type = None
layer_manager_gw_schema.subscription_type = None

