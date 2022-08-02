import gc

import pytest

from pytest_bdd import given, then, scenarios, parsers
from app.lib.exchangeConnector import Connector

import logging
logging.basicConfig(format="%(asctime)s: %(levelname)-8s : %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


def pytest_bdd_before_scenario(request, feature, scenario):
    logger.info(f"[SCENARIO]============================= Executing Scenario: {scenario.name}=============================")


def pytest_bdd_after_scenario(request, feature, scenario):
    gc.collect()


def pytest_bdd_before_step(request, feature, scenario, step, step_func):
    logger.info(f"[STEP]------------------------------Executing Step: {step.name}------------------------------")


@pytest.fixture
def context():
    logger.debug("****Setting up for execution****")
    #setup
    context = Connector()
    yield context

    #tear down
    context = None


@given(parsers.parse('I am connected to spot exchange "{endPointType}" api'))
# @given('I am connected to spot exchange "<endPointType>" api')
def connectToSpotExchange(context, endPointType):
    logger.debug("Executing connectToSpotExchange...")
    status = context.connectToExchange(isPublic=True) if endPointType == "public" else context.connectToExchange(isPrivate=True)
    try:
        assert status is True
    except AssertionError:
        logger.error(f"[FAIL]: Connect to Spot Exchange Step failed")
        pytest.fail(f"[FAIL]: Connect to Spot Exchange Step failed")


@then('validate the api response')
def assertResponse(context):
    logger.debug("Executing assertResponse...")
    try:
        assert context.validateResponse(context.response) is True
    except AssertionError:
        logger.error(f"[FAIL]: Response Validation Step failed")
        pytest.fail(f"[FAIL]: Response Validation Step failed")


@then(parsers.parse('Response "{valueToBeVerified}" is "{condition}" "{expectedValue}"'))
def assertResponseFieldsWithCondition(context, valueToBeVerified, condition, expectedValue):
    logger.debug("Executing assertResponseFieldsWithCondition...")
    try:
        if valueToBeVerified == "status" and condition == "equal to":
            context.validateResponse(context.response, verifyStatus=int(expectedValue))
        elif condition == "less than":
            if valueToBeVerified == "time":
                context.validateResponse(context.response, verifyMaxResponseTime=int(expectedValue))
        # more comparison structure can be added here
    except AssertionError:
        logger.error(f"[FAIL]: Response Validation Step failed while validating fields with condition")
        pytest.fail(f"[FAIL]: Response Validation Step failed while validating fields with condition")


@then(parsers.parse('Response "{responseSection}" has "{listOfKeyValuePairsToVerify}"'))
def assertResponseFields(context, responseSection, listOfKeyValuePairsToVerify):
    logger.debug("Executing assertResponseFields...")
    convertedListOfKeyValuePair = list(eval(listOfKeyValuePairsToVerify))
    try:
        if responseSection == "header":
            assert context.validateResponse(context.response, listOfHeadersToVerify=convertedListOfKeyValuePair) is True
        if responseSection == "body":
            assert context.validateResponse(context.response, listOfBodyParamsToVerify=convertedListOfKeyValuePair) is True
    except AssertionError:
        logger.error(f"[FAIL]: Response Validation Step failed while validating body fields")
        pytest.fail(f"[FAIL]: Response Validation Step failed while validating body fields")




