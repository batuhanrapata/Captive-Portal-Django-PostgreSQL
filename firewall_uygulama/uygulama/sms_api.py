from twilio.rest import Client
import os

from dotenv import load_dotenv

load_dotenv()  # .env dosyasını oku

Service_SID = os.environ.get('Service_SID')  # .env dosyasından okunan değerler
Twilio_Account_SID = os.environ.get(' ')
Auth_Token = os.environ.get('Auth_Token')

client = ""
    #Client(Twilio_Account_SID, Auth_Token)  # twilio client


def send_verification(email):  # mail gönder
    verification = client.verify \
        .v2 \
        .services(Service_SID) \
        .verifications \
        .create(to=email, channel='email', locale='tr')
    return verification.status == 'pending'


def check_verification_token(email, token):  # mail doğrula
    check = client.verify \
        .v2 \
        .services(Service_SID) \
        .verification_checks \
        .create(to=email, code=token)
    return check.status == 'approved'


def send_otp(tel_no):  # sms gönder
    verification = client.verify \
        .v2 \
        .services(Service_SID) \
        .verifications \
        .create(to=tel_no, channel='sms', locale='tr')
    return verification.status == 'pending'


def chech_otp(tel_no, token):  # sms doğrula
    check = client.verify \
        .v2 \
        .services(Service_SID) \
        .verification_checks \
        .create(to=tel_no, code=token)
    return check.status == 'approved'
####acil acil acil api lazım