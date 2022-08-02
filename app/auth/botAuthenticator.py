import pyotp
from argparse import ArgumentParser
import json
import os


def getOtp(setupKey: str = ""):
    """
    :param setupKey: Setup key from your 2FA sign-in Setup
                     Send an empty string '' to generate OTP for API_SECRET
    :return: one time password
    """
    if setupKey == "":
        jsonData = json.load(open(os.getcwd().split("app")[0]+"app/auth/info.json", 'r'))
        setupKey = jsonData["SETUP_KEY"]
    otp = pyotp.TOTP(setupKey).now()
    print(otp)
    return otp


if __name__ == "__main__":
    """
        Acecss to main is given here to generate OTP code while doing a new project setup
    """
    parser = ArgumentParser(description="Fetch the OTP for a given SETUP KEY")
    parser.add_argument("-s", "--setupKey", required=True, help="Setup key from your 2FA sign-in Setup")
    setupKey = parser.parse_args().setupKey
    getOtp(setupKey=setupKey)
