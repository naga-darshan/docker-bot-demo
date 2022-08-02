import app.util.api.path.public as publicPaths
import app.util.api.path.private as privatePaths
import requests
from app.auth.botAuthenticator import getOtp
from app.util.requestHandler import privateApiRequest, publicApiRequest, _decode
import json
import os
import time

import logging

logging.basicConfig(format="%(asctime)s: %(levelname)-8s : %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

jsonData = json.load(open((os.getcwd().split("app")[0] + "app/auth/info.json"), 'r'))


class Connector(object):
    apiUrl = ""
    apiKey = ""
    apiSec = ""

    def __init__(self):
        self.apiUrl = jsonData["HOST"]
        self.apiKey = jsonData['API_KEY']
        self.apiSec = jsonData['API_SECRET']
        self.trading2FA = jsonData['TRADING_2FA']

    def connectToExchange(self, isPublic=False, isPrivate=False):
        """
        Performs a test connection into the server to test the network/connection validity
        :param isPublic: Boolean
        :param isPrivate: Boolean
        :return: Assertion
        """
        if isPublic:
            assert self.__testPublicConnectionValidity(self.apiUrl) is 200
            logger.info(f"[PASS]: Connected to Public API")
        elif isPrivate:
            assert self.__testPrivateConnectionValidity(self.apiUrl, self.apiKey, self.apiSec) is 200
            logger.info(f"[PASS]: Connected to Private API")
        return True

    def __testPublicConnectionValidity(self, apiUrl):
        return publicApiRequest(apiUrl).status_code

    def __testPrivateConnectionValidity(self, apiUrl, apiKey, apiSec):
        return privateApiRequest(baseUrl=apiUrl, urlPath='', data={"nonce": str(int(1000 * time.time()))},
                                 apiKey=apiKey, apiSec=apiSec).status_code

    def getServerTime(self):
        """
        Fetch server time from public api
        :return: response
        """
        return publicApiRequest(baseUrl=self.apiUrl, urlPath=publicPaths.ServerTime)

    def getTradePairInfo(self, tradePair):
        """
        Fetch info for a given trade pair from public api
        :param tradePair: trade pair combo
        :return: response
        """
        return publicApiRequest(baseUrl=self.apiUrl, urlPath=publicPaths.Ticker, params=f"?pair={tradePair}")

    def getSpotOpenOrders(self):
        """
        Fetch all the open orders on the user account for spot exchange
        :return: response for spot open orders
        """
        data = {
            "nonce": str(int(1000 * time.time())),
            "trades": True,
            "2fa": _decode(self.trading2FA)  # "2fa" is the key used for 2-factor-authentication;
        }

        response = privateApiRequest(baseUrl=self.apiUrl,
                                     urlPath=privatePaths.OpenOrders,
                                     data=data,
                                     apiKey=self.apiKey,
                                     apiSec=self.apiSec)

        return response

    def validateResponse(self,
                         response: requests.models.Response,
                         verifyStatus=-1,
                         verifyMaxResponseTime=-1,
                         listOfHeadersToVerify: list = None,
                         listOfBodyParamsToVerify: list = None):
        """
        This function will help in performing all the necessary validations on the generated response
        :param response:
        :param verifyStatus:
        :param verifyMaxResponseTime:
        :param listOfHeadersToVerify:
                [{key: expectedValue},{key: expectedValue},{key: expectedValue}....]
        :param listOfBodyParamsToVerify:
                [{path.to.node: expectedValue},{path.to.node: expectedValue},{path.to.node: expectedValue}....]
        :return: Assertion Status
        """

        assertionStatus = True

        assert response is not {}
        logger.info(f"[PASS]: Valid Response received")

        if verifyStatus > 0:
            try:
                assert response.status_code == verifyStatus
                logger.info(
                    f"[PASS]: Response Status code matches expected; Expected value: {str(verifyStatus)} | Actual value: {str(response.status_code)}")
            except AssertionError:
                assertionStatus = False
                logger.info(
                    f"[FAIL]: Response Status code does not match expected; Expected value: {str(verifyStatus)} | Actual value: {str(response.status_code)}")

        if verifyMaxResponseTime > 0:
            try:
                assert response.elapsed.total_seconds() < verifyMaxResponseTime
                logger.info(
                    f"[PASS]: Response time with-in expected max time; Expected value: {str(verifyMaxResponseTime)} | Actual value: {str(response.elapsed.total_seconds())}")
            except AssertionError:
                assertionStatus = False
                logger.info(
                    f"[FAIL]: Response time not with-in expected max time; Expected value: {str(verifyMaxResponseTime)} | Actual value: {str(response.elapsed.total_seconds())}")

        if listOfHeadersToVerify is not None:
            for _ in range(len(listOfHeadersToVerify)):
                curHeader = listOfHeadersToVerify[_]
                for k, v in curHeader.items():
                    try:
                        assert response.headers[k] == v
                        logger.info(
                            f"[PASS]: Field [{k}] in header matches expected; Expected value: {str(v)} | Actual value: {str(response.headers[k])}")
                    except AssertionError:
                        assertionStatus = False
                        logger.error(
                            f"[FAIL]: Field [{k}] in header does not match expected; Expected value: {str(v)} | Actual value: {str(response.headers[k])}")

        if listOfBodyParamsToVerify is not None:

            for _ in range(len(listOfBodyParamsToVerify)):
                curBodyParam = listOfBodyParamsToVerify[_]
                for k, v in curBodyParam.items():  # k ==> path.to.node| v ==> expectedValue
                    pathItems = str(k).split(".")
                    if len(pathItems) > 0:
                        try:
                            _ = response.json()
                            for i in range(len(pathItems)):
                                # response.json()["path"][To"]["node"] = expectedValue
                                try:
                                    _ = _[str(pathItems[i])]
                                    # logger.debug(f"_ = {str(_)}")
                                except KeyError:
                                    assertionStatus = False
                                    logger.error(f"[FAIL]: Field [{str(pathItems[len(pathItems)-1])}] not present")

                            if v == 'non-zero-number':
                                assert int(_) > 0  # verify that tag exists
                                logger.info(f"[PASS]: Field [{pathItems[len(pathItems)-1]}] is a non-zero: {str(_)}")
                            elif v == 'non-empty-string':
                                assert len(str(_)) > 0  # verify that tag exists
                                logger.info(f"[PASS]: Field [{pathItems[len(pathItems)-1]}] is a non-empty: {str(_)}")
                            else:
                                assert _ == v  # exact value match
                                logger.info(
                                        f"[PASS]: Field [{pathItems[len(pathItems)-1]}] matches expected; Expected value: {str(v)} | Actual value: {str(_)}")
                        except AssertionError:
                            assertionStatus = False
                            logger.error(
                                f"[FAIL]: Field [{pathItems[len(pathItems)-1]}] does not match expected; Expected value: {str(v)} | Actual value: {str(_)}")
                    else:
                        assertionStatus = False
                        logger.error(
                            f"[FAIL]: Invalid Path.To.Node sent as input for validation, verify test step in feature file")

        return assertionStatus

