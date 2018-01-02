import json
import requests
import time

def get_bitcoin_balance(address):
	'''
	Given an address returns BTC balance
	'''
	requestURL = "https://blockchain.info/rawaddr/{}".format(address)

	#Try 5 times, incase server API is busy.
	for x in range(0, 5):
		payload = requests.get(requestURL)
		payload = json.loads(payload.text)

		if payload['final_balance'] is not None:
			return float(payload['final_balance'])/100000000 #Result is in Satoshi
		else:
			time.sleep(3)
	return None
