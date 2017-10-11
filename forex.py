#!/usr/bin/env python3
import json
import requests
import time
import sys

usd_forex_data_source = "https://api.fixer.io/latest?base=USD"
usd_forex_data = None

def convertUSD(currency, amount):
	'''
	Converts amount to target currency based on USD
	'''
	#Get forex json data if not available, global save to minimise API calls
	global usd_forex_data
	if usd_forex_data == None:
		usd_forex_data = getUSDForex()
	
	#Convert to target unless already USD
	if currency is not "USD":
		return float(amount)*usd_forex_data['rates'][currency]
	else:
		return float(amount)
	
def getUSDForex():
	'''
	Retrieve forex data from the source
	'''
	#Try to retrieve forex
	for x in range(0,5):
		payload = requests.get(usd_forex_data_source).json()
		if payload != "" or not None:
			return payload
		time.sleep(10)

	print("Failed to retrieve forex")
	sys.exit()