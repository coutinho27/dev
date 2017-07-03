from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = "AC2f88e71e257b6db99183ca43ae4b7000"
auth_token = "48a57e95a4d23583039c7d6d7a15d4a0"
client = Client(account_sid, auth_token)

#Teste com telefone do Paulo
message = client.api.account.messages.create(to="+5531994766248",
                                             from_="+5531994289741",
                                             body="Hello there!")