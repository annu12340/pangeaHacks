import os
from twilio.rest import Client
from dotenv import load_dotenv
from utils.get_token_from_vault import get_token
load_dotenv()


def send_twilio_msg(number, message):

    account_sid = get_token("pvi_zkylvdcedngam63jeb4aia66izpekiiv")
    auth_token = get_token("pvi_yrhe57dmffh7734g2jecw5gldt474z44")

    client = Client(account_sid, auth_token)

    message = client.messages.create(from_="+12542384124", body=message, to=number)
    print(message.sid)
