# services.py

from twilio.rest import Client
from backend.settings import TwilioConstants,DEBUG
# from basettings import DEBUG
class SmsHelper:

    def send_otp(phone_number):
        if  DEBUG:
            return True
        
        client = Client(TwilioConstants.TWILIO_ACCOUNT_SID, TwilioConstants.TWILIO_AUTH_TOKEN)
        verification = client.verify.services(TwilioConstants.TWILIO_SERVICE_SID).verifications.create(to=phone_number, channel='sms')

    def verify_otp(phone_number, otp):
        if DEBUG and otp == "123456":
            return "approved"
        client = Client(TwilioConstants.TWILIO_ACCOUNT_SID, TwilioConstants.TWILIO_AUTH_TOKEN)
        verification_check = client.verify.services(TwilioConstants.TWILIO_SERVICE_SID).verification_checks.create(to=phone_number, code=otp)
        return verification_check.status
