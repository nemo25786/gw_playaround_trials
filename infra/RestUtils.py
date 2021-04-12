import json
from logging import Logger
import requests


def improved_get(log: Logger, url, params=None, headers=None):
    log.debug("sending GET request to URL: {} with params: {}".format(url, params))

    try:
        response = requests.get(url=url, params=params, headers=headers)
    except Exception as e:
        log.error("error in sending GET request due to {}".format(str(e)))
        raise e

    log.debug("got response for GET request from url: {} as: {}".format(url, response.text))

    return response

def improved_post(log: Logger, url, headers=None, request_json=None):
    log.debug("sending POST request to URL: {} with request json: {}".format(url, json.dumps(request_json, indent=2)))

    try:
        response = requests.post(url=url, headers=headers, json=request_json)
    except Exception as e:
        log.error("error in sending POST request due to {}".format(str(e)))
        raise e

    log.debug("got response for POST request from url: {} with status code {} as: {}\n".format(url, response.status_code,
                                                                                              response.text))

    return response


def improved_put(log: Logger, url, headers=None, request_json=None):
    log.debug("sending PUT request to URL: {} with request json: {}".format(url, json.dumps(request_json, indent=2)))

    try:
        response = requests.put(url=url, headers=headers, json=request_json)
    except Exception as e:
        log.error("error in sending PUT request due to {}".format(str(e)))
        raise e

    log.debug("got response for PUT request from url: {} with status code {} as: {}\n".format(url, response.status_code,
                                                                                              response.text))

    return response

def improved_delete(log: Logger, url):
    log.debug("sending DELETE request to URL: {}".format(url))

    try:
        response = requests.delete(url=url)
    except Exception as e:
        log.error("error in sending DELETE request due to {}".format(str(e)))
        raise e

    log.debug("got response for DELETE request from url: {} as: {}\n".format(url, response.text))

    return response


class Error(Exception):
    pass

class ServerError(Error):
    pass

class ClientError(Error):
    pass

Error_dict = {
    "ClientError": ClientError,
    "ServerError": ServerError,
}

def is_response_ok(status_code):
    if int(status_code) >= 400 and int(status_code) < 500:
        raise Error_dict["ClientError"]
    elif int(status_code) >= 500:
        raise Error_dict["ServerError"]
    else:
        return True


