from twilio.rest import Client
import os

from dotenv import load_dotenv

load_dotenv()

Service_SID = os.environ.get('Service_SID')
Twilio_Account_SID = os.environ.get('Twilio_Account_SID')
Auth_Token = os.environ.get('Auth_Token')

client = Client(Twilio_Account_SID, Auth_Token)


def send_verification(email):
    verification = client.verify \
        .v2 \
        .services(Service_SID) \
        .verifications \
        .create(to=email, channel='email')
    return verification.sids


def check_verification_token(email, token):
    check = client.verify \
        .v2 \
        .services(Service_SID) \
        .verification_checks \
        .create(to=email, code=token)
    return check.status == 'approved'
