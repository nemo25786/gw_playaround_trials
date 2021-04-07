import ssl
from socket import socket

import requests


def improved_get(log, url, params=None, headers=None):
    log.info("sending GET request to URL: {} with params: {}".format(url, params))

    try:
        response = requests.get(url=url, params=params, headers=headers)
    except Exception as e:
        log.info("error in sending GET request due to {}".format(str(e)))
        raise e

    log.info("got response for GET request from url: {} as: {}".format(url, response.text))

    return response

def improved_post(log, url, headers=None, data=None, json=None):
    log.info("sending POST request to URL: {} with data: {}".format(url, data))

    try:
        response = requests.post(url=url, data=data, headers=headers, json=json)
    except Exception as e:
        log.info("error in sending POST request due to {}".format(str(e)))
        raise e

    log.info("got response for POST request from url: {} as: {}\n".format(url, response.text))

    return response

def improved_delete(log, url):
    log.info("sending DELETE request to URL: {}".format(url))

    try:
        response = requests.delete(url=url)
    except Exception as e:
        log.info("error in sending DELETE request due to {}".format(str(e)))
        raise e

    log.info("got response for DELETE request from url: {} as: {}\n".format(url, response.text))

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



