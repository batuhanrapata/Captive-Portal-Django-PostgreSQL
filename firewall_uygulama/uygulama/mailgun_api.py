import requests
import os
import random
import string
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("MAILGUN_API_KEY")
domain = os.environ.get("MAILGUN_DOMAIN")


def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))


def send_simple_message(email):
    otp = generate_otp()
    requests.post(
        "https://api.mailgun.net/v3/sandboxa49efa1327944ef6bfcaa532f41b6130.mailgun.org/messages",
        auth=("api", api_key),
        data={"from": "Mailgun Sandbox <postmaster@sandboxa49efa1327944ef6bfcaa532f41b6130.mailgun.org>",
              "to": [email],
              "subject": "Your OTP is " + otp + "",
              "template": "otp",
              "h:X-Mailgun-Variables": '{ "code" : "' + otp + '"}'})
    return otp


def check_otp(otp):
    return otp == otp
