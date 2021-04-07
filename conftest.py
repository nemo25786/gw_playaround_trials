import os
import sys
import time
import pytest
import datetime
import allure
import requests

from infra.RestUtils import improved_get, is_response_ok
from infra.Utils import format_filename, str2bool
from ccst_config_reader import ConfigReader
import logging
from GrafanaSnapshot import SnapshotFace
from jsonformatter import JsonFormatter

ZAPI_TEST_STATUS = {
             "pass": {"id": 1},
             "fail": {"id": 2},
             "unexecuted": {"id": -1}
}

STRING_FORMAT = '''{
    "Name":            "name",
    "Levelname":       "levelname",
    "Module":          "module",
    "Lineno":          "lineno",
    "FuncName":        "funcName",
    "Asctime":         "asctime",
    "ThreadName":      "threadName",
    "Message":         "message"
}'''

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function", autouse=False)
def get_function_name(request):
    time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    function_name = format_filename(request.node.nodeid) + "_" + time

    return function_name


@pytest.fixture(scope='function', autouse=False)
def get_log(get_function_name, logging_level=logging.DEBUG):
    time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    logger_name = get_function_name

    test_logger = logging.getLogger(logger_name)
    formatter = JsonFormatter(STRING_FORMAT)
    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(formatter)
    test_logger.addHandler(sh)
    test_logger.setLevel(logging_level)

    test_logger.info("*"*41 + 'TEST_SETUP' + "*"*40)
    test_logger.info("initializing setUp operations for test {} at ".format(get_function_name, time))
    set_warning_to_all_loggers_except(logger_name)
    yield test_logger
    test_logger.info("ending logging for test for function {}".format(get_function_name))

@pytest.fixture(scope="function", autouse=False)
def get_config(get_log):
    if str2bool(os.environ['EXTERNAL']) == True:
        config_file_name = "external_config.ini"
        get_log.debug("running in external mode")
    else:
        config_file_name = "config.ini"
        get_log.debug("running in internal mode")

    project_config = ConfigReader.get_config(config_file_name=config_file_name)

    yield project_config

@pytest.fixture(scope="function", autouse=False)
def get_status(request, get_log):
    get_log.info("*"*41 + 'TEST_BODY' + "*"*41)
    yield
    if request.node.rep_setup.failed:
        get_log.exception("error in setUp, please check log for errors and fix them before trying again")
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            get_log.error("TEST FAILED".format(request.node.nodeid))
        else:
            get_log.info("TEST PASSED".format(request.node.nodeid))

    get_log.info("*"*39 + 'TEST_TEARDOWN' + "*"*39)

@pytest.fixture(scope="function", autouse=False)
def get_grafana_snapshot(request, get_function_name, get_config, get_log):
    epoc_time_from_start = round(time.time() * 1000)

    get_log.info("grafana metrics beginning at {}".format(time.ctime(time.time())))
    try:
        grafana = SnapshotFace(auth=(get_config["AUTH"]["GRAFANA_USER"], get_config["AUTH"]["GRAFANA_PASSWORD"]),
                               # auth=get_config["AUTH"]["GRAFANA_API_KEY"],
                               port=get_config["SERVICES"]["grafana_internal_port"],
                               host=get_config["SERVICES"]["grafana_server_internal"],
                               protocol="http")
    except Exception as e:
        get_log.warning("cannot connect to Grafana API server, will not add metrics to report")

    yield
    epoc_time_end = round(time.time() * 1000)
    print(epoc_time_from_start)
    print(epoc_time_end)
    get_log.info("grafana metrics ending at {}".format(time.ctime(time.time())))

    try:
        results = grafana.snapshots.create_snapshot(test_name=format_filename(request.node.nodeid), tags=get_config["general"]["grafana_tag"], time_from=epoc_time_from_start, time_to=epoc_time_end,
                                                expires=None)
    except Exception as e:
        get_log.warning("unable to create snapshot due to {}, snapshot will not be added to report".format(str(e)))
        return

    for result in results:
        link = "http://" + get_config["SERVICES"]["grafana_server_external"] + ":" + get_config["SERVICES"]["grafana_external_port"] + result
        get_log.info("link for snapshot saved at link: {}".format(link))
        allure.attach(name=get_function_name + "_grafana_metrics", extension=allure.attachment_type.URI_LIST, body=link)


def set_warning_to_all_loggers_except(logger_name):
    formatter = JsonFormatter(STRING_FORMAT)
    sh = logging.StreamHandler(stream=sys.stdout)
    for name in logging.root.manager.loggerDict:
        if name not in logger_name:
            logger = logging.getLogger(name)
            sh.setFormatter(formatter)
            logger.addHandler(sh)
            logger.setLevel(logging.WARNING)


@pytest.fixture(scope='function', autouse=False)
def check_connect_to_server(get_function_name, get_log, get_config, server):
    response = improved_get(log=get_log, url=get_config["SERVICES"][server], params={})

    assert response.status_code != requests.codes.not_found
