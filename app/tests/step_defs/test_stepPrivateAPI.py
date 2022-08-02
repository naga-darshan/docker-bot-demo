from pytest_bdd import when, scenarios, parsers

import logging
logging.basicConfig(format="%(asctime)s: %(levelname)-8s : %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

scenarios("../features/privateApi.feature")


@when(parsers.parse('I retrieve the "{orderType}" orders for the account'))
def retrieveOrders(context, orderType):
    logger.debug("Executing retrieveOrders...")
    if orderType == 'open':
        context.response = context.getSpotOpenOrders()


