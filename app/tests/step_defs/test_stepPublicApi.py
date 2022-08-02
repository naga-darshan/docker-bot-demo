from pytest_bdd import when, scenarios, parsers
import pytest
import logging
logging.basicConfig(format="%(asctime)s: %(levelname)-8s : %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

scenarios("../features/publicApi.feature")


@when(parsers.parse('I retrieve the server time'))
def retrieveServerTime(context):
    logger.debug("Executing retrieveServerTime...")
    try:
        context.response = context.getServerTime()
    except:
        pytest.fail(f"[FAIL]: Response Validation Step failed while validating body fields")



@when(parsers.parse('I retrieve the "{tradePair}" trade pair'))
# @when('I retrieve the "<tradePair>" trade pair')
def retrieveTradePairInfo(context, tradePair):
    try:
        logger.debug("Executing retrieveTradePairInfo...")
        context.response = context.getTradePairInfo(tradePair)
    except:
        pytest.fail(f"[FAIL]: Response Validation Step failed while validating body fields")
