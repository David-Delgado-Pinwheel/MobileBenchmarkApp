from twilio.rest import Client
 
account_sid = 'AC3ca71a03dd1eafa8253c304842596cef' 
auth_token = '[AuthToken]' 
client = Client(account_sid, auth_token) 
 
message = client.messages.create(         
                              to='+15127539633'
                          ) 
 
print(message.sid)