from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = "AC2xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
auth_token = "564cdxzczxczxczxca5646543214"
client = Client(account_sid, auth_token)

#Teste com telefone do Paulo
message = client.api.account.messages.create(to="+5531994766248",
                                             from_="+5531994289741",
                                             body="Hello there!")