import json
import requests
from modules import wallets

cryptodata = {}

def getCrypto(token):
	global cryptodata
	if not token in cryptodata:
		token = token.strip()
		requestURL = "http://www.coincap.io/page/{}".format(token)
		payload = requests.get(requestURL)
		cryptodata[token] = json.loads(payload.text)
	return cryptodata[token]

def getCryptoValueETH(token):
	data = getCrypto(token)
	return data['price_eth']

def getCryptoValueBTC(token):
	data = getCrypto(token)
	return data['price_btc']

def getCryptoValueUSD(token):
	data = getCrypto(token)
	return data['price_usd']

def getCryptoVolume(token):
	data = getCrypto(token)
	return data['volume']

def getCryptoMarketCap(token):
	data = getCrypto(token)
	return data['market_cap']

def getEthUSDValue(account):
	ethUSDPrice = getCryptoValueUSD("ETH")
	ethWalletBalance = wallets.getEthereumBalance(account['wallet'])
	return ethWalletBalance*ethUSDPrice

def getBitUSDValue(address):
	btcUSDPrice = getCryptoValueUSD("BTC")
	bitWalletBalance = wallets.getBitcoinBalance(address)
	return bitWalletBalance*btcUSDPrice

def getTokenUSDValue(account, token):
	tokenUSDPrice = getCryptoValueUSD(token)
	tokenWalletBalance = wallets.getTokenBalance(token, account['wallet'])
	return tokenWalletBalance*tokenUSDPrice
