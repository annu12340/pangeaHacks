import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


def send_twilio_msg(number, message):

    account_sid = os.getenv("TWILIO_ACCOUNT")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    client = Client(account_sid, auth_token)

    message = client.messages.create(from_="+12542384124", body=message, to=number)
    print(message.sid)
