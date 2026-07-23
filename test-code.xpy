##############################################################################################
############################### Email TEST CODE ####################################################################################################
# from brevo import Brevo
# from brevo.transactional_emails import (
#     SendTransacEmailRequestSender,
#     SendTransacEmailRequestToItem,
# )
# client = Brevo(api_key="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")
# result = client.transactional_emails.send_transac_email(
#     subject="Hello from Brevo!",
#     html_content="<html><body><p>Hello,</p><p>This is my first transactional email.</p></body></html>",
#     sender=SendTransacEmailRequestSender(
#         name="Alex from Brevo",
#         email="hello@tradeb2b.online",
#     ),
#     to=[
#         SendTransacEmailRequestToItem(
#             email="akshatguptatom@gmail.com",
#             name="Akshat Gupta",
#         )
#     ],
# )
# print("Email sent. Message ID:", result.message_id)

##############################################################################################
############################### SMS TEST CODE ####################################################################################################

import requests

API_KEY = "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"

url = "https://api.brevo.com/v3/transactionalSMS/send"

headers = {
    "accept": "application/json",
    "api-key": API_KEY,
    "content-type": "application/json",
}

payload = {
    "sender": "TradeB2B",
    "recipient": "+918881316612",
    "content": "Your OTP is 123987. Use it to verify your account. Please do not share it with anyone.",
    "type": "transactional"
}

response = requests.post(url, json=payload, headers=headers)

print(response.status_code)
print(response.text)