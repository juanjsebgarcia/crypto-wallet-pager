import json
import requests
import time

ETHERSCAN_API = json.loads(open('settings.json', 'r').read())['Etherscan_api']

tokencontracts = None

def loadContracts():
	'''
	Loads contracts from MEW git, falls back to local instance if fails
	'''
	global tokencontracts
	if tokencontracts is None:
		try:
			contracts = requests.get('https://raw.githubusercontent.com/kvhnuke/etherwallet/mercury/app/scripts/tokens/ethTokens.json').json()
		except:
			file = open('ethTokens.json', 'r')
			contracts = json.loads(file.read())
	return contracts

def returnTokenAddress(ticker):
	'''
	Given token ticker, returns matching contract address
	'''
	tokenlist = loadContracts()
	for token in tokenlist:
		if token['symbol'] == ticker.upper():
			return token['address']
	return None

def getTokenBalance(token, address):
	'''
	Takes token ticker and contract address and returns matching ERC20 token balance.
	'''
	token = token.strip().upper()
	tokenAddress = returnTokenAddress(token)
	requestURL = "https://api.tokenbalance.com/balance/"+tokenAddress+"/"+address

	#Try 5 times, incase server API is busy.
	for x in range(0, 5):
		payload = requests.get(requestURL)
		balance = float(payload.text)
		if balance != "" or not None:
			return balance
		else:
			time.sleep(5)
	return None

def getEthereumBalance(address):
	'''
	Given an address returns ETH balance
	'''
	requestURL = "https://api.etherscan.io/api?module=account&action=balance&address={}&tag=latest&apikey={}".format(address, ETHERSCAN_API)

	#Try 5 times, incase server API is busy.
	for x in range(0, 5):
		payload = requests.get(requestURL)
		payload = json.loads(payload.text)

		if payload['message'] == "OK":
			ethBalance = float(payload['result'])/1000000000000000000 #Result is in Wei
			return ethBalance
		else:
			time.sleep(5)
	return None
