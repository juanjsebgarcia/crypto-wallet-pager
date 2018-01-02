import json
from twilio.rest import Client

try:
	account_sid = json.loads(open('settings.json', 'r').read())['Twilio_account_sid']
	auth_token = json.loads(open('settings.json', 'r').read())['Twilio_auth_token']
	source_number = json.loads(open('settings.json', 'r').read())['Twilio_source_number']
	twilio_activate = True
except:
	print("Twilio failed to load settings")

def send_sms(recipient, message):
	'''
	Send SMS using Twilio
	'''
	global twilio_activate
	if twilio_activate:
		client = Client(account_sid, auth_token)
		client.messages.create(
		to=recipient,
		from_=source_number,
		body=message,
		)
	else:
		return None
