#!/usr/bin/env python3
import json
import requests
import time
import sys

usd_forex_data_source = "https://api.fixer.io/latest?base=USD"
usd_forex_data = None

crypto_data_source = "https://api.coinmarketcap.com/v1/ticker/?limit=0"
crypto_data = None

def from_usd(currency, amount):
	'''
	Converts amount to target currency based on USD
	'''
	#Get forex json data if not available, global save to minimise API calls
	global usd_forex_data
	if usd_forex_data == None:
		usd_forex_data = get_usd_forex()

	#Convert to target unless already USD
	if currency is not "USD":
		return float(amount)*usd_forex_data['rates'][currency]
	else:
		return float(amount)


def get_usd_forex():
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


def get_usd_value(token):
	global crypto_data
	if crypto_data is None:
		crypto_data = get_crypto_data()

	for ticker in crypto_data:
		if ticker['symbol'] == token:
			return float(ticker['price_usd'])

	return 0


def get_crypto_data():
	'''
	Retrieve forex data from the source
	'''
	#Try to retrieve forex
	for x in range(0,5):
		payload = requests.get(crypto_data_source).json()
		if payload != "" or not None:
			return payload
		time.sleep(10)

	print("Failed to retrieve coinmarketcap")
	sys.exit()
