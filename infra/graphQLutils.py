class GraphQLError(Exception):
    pass


class QueryError(GraphQLError):
    pass


class MutationError(GraphQLError):
    pass


def send_query(endpoint, query, logger):
    logger.debug("attempting to send query with body {}".format(query))
    try:
        data = endpoint(query=query)
    except Exception as e:
        logger.exception("error in sending query with message {}".format(str(e)))
        raise QueryError

    if "errors" in data:
        logger.error("fail in query, received response {}".format(data))
        return None

    response = query+data
    logger.debug("received data from query {}".format(response))
    return response


def send_mutation(endpoint, mutation, logger):
    logger.debug("attempting to send mutation with body {}".format(mutation))
    try:
        data = endpoint(query=mutation)
    except Exception as e:
        logger.excpetion("error in sending query with message {}".format(str(e)))
        raise MutationError

    if "errors" in data:
        logger.error("fail in mutation, received response {}".format(data))
        return None

    response = mutation+data

    logger.debug("received data from mutation {}".format(response))
    return response
