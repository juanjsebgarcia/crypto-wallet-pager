import json
import requests
from modules import wallets

def getCrypto(token):
	token = token.strip()
	requestURL = "http://www.coincap.io/page/{}".format(token)
	payload = requests.get(requestURL)
	return json.loads(payload.text)	

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

def getTokenUSDValue(account, token):
	tokenUSDPrice = getCryptoValueUSD(token)
	tokenWalletBalance = wallets.getTokenBalance(token, account['wallet'])
	return tokenWalletBalance*tokenUSDPrice