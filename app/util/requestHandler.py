import urllib.parse
import hashlib
import hmac
import base64

from argparse import ArgumentParser
import requests


def getSignature(urlpath, data, secret):

    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


def privateApiRequest(baseUrl, urlPath, data, apiKey, apiSec):
    headers = {}
    headers['API-Key'] = apiKey
    headers['API-Sign'] = getSignature(urlPath, data, apiSec)  # as defined in the 'Authentication' section
    response = requests.post(f"https://{_decode(baseUrl)}{urlPath}", headers=headers, data=data)
    return response


def publicApiRequest(baseUrl, urlPath='', params=''):
    response = requests.get(f"https://{_decode(baseUrl)}{urlPath}{params}")
    return response


def _decode(inputStr):
    return (base64.b64decode(inputStr.encode('ascii'))).decode('ascii')


def _encode(inputStr):
    code = (base64.b64encode(inputStr.encode('ascii'))).decode('ascii')
    print(code)
    return code


if __name__ == "__main__":
    """
        Acecss to main is given here to generate encoded/decoded message while doing a new project setup
    """
    parser = ArgumentParser(description="Encode your string/password")
    parser.add_argument("-e", "--inputStr", required=True, help="Input string/password")
    inputStr = parser.parse_args().inputStr
    _encode(inputStr=inputStr)

