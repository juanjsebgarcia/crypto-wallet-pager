#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
import sys
from modules import wallets
from modules import cryptos
from modules import forex
from modules import tools

#Global Variables
today = datetime.date.today()
SMS = False
EMAIL = False

#Set runtime variables
if len(sys.argv) > 1:
	for arg in sys.argv:
		if arg == "sms":
			from notifications import sms
			SMS = True
		if arg == "email":
			from notifications import mail
			EMAIL = True

try:
	base_currency = json.loads(open('settings.json', 'r').read())['Base_currency']
except:
	print("Failed to load base currency from settings.json defaulting to USD")
	base_currency = 'USD'
	sys.exit()

try:
	accounts = json.loads(open('accounts.json', 'r').read())
except:
	print("JSON loading error for accounts.json")
	sys.exit()

#Track fiat total across all wallets registered
contentTotal = ""
walletsTotal = 0

#FOR EACH ACCOUNT
for account in accounts:
	#Track fiat balance in each wallet
	walletBalance = 0
	walletString = ""

	#ETHEREUM
	try:
		ethUSDValue = cryptos.getEthUSDValue(account)
		ethLocalValue = forex.convertUSD(account['currency'], ethUSDValue)
		if ethLocalValue > 0:
			walletBalance += ethLocalValue
			walletString += "ETH: ~{} {}\n".format(tools.prettyOutput(ethLocalValue), account['currency'])
			walletsTotal += ethUSDValue
	except:
		print("ETH balance retrieval failed for wallet {}".format(account['wallet']))

	#ERC20 TOKENS
	#If tokens exist, check their formatting and attempt to retrieve values
	if account['tokens'] is not None:
		try:
			tokens = account['tokens'].split(",")
			for token in tokens:
				try:
					tokenUSDValue = cryptos.getTokenUSDValue(account, token.strip())
					tokenLocalValue = forex.convertUSD(account['currency'], tokenUSDValue)
					if tokenLocalValue > 0:
						walletBalance += tokenLocalValue
						walletString += "{}: ~{} {}\n".format(str(token), tools.prettyOutput(tokenLocalValue), account['currency'])
						walletsTotal += tokenUSDValue
				except:
					print("Error loading token data for {}".format(token))
		except:
			print("Error loading tokens for address {}".format(account['wallet']))

	#Bitcoin
	#If bitcoin wallet
	if 'bitcoin' in account:
		bitLocalValue = 0
		try:
			bit_addresses = account['bitcoin'].split(",")
			for address in bit_addresses:
				try:
					bitUSDValue = cryptos.getBitUSDValue( address.strip())
					bitLocalValue += forex.convertUSD(account['currency'], bitUSDValue)
				except:
					print("Error loading token data for {}".format(token))
			if bitLocalValue > 0:
				walletBalance += bitLocalValue
				walletString += "{}: ~{} {}\n".format('BTC', tools.prettyOutput(bitUSDValue), account['currency'])
				walletsTotal += bitUSDValue
		except:
			print("Error loading bitcoin for address(es) {}".format(account['bitcoin']))

	#PREPARE EXPORT CONTENT
	walletTotalClean = tools.prettyOutput(walletBalance)
	header = account['name'] +" Crypto Wallet\n"
	date =  "{:%d %b %Y}".format(today)+"\n"
	total = "TOTAL: ~{} {}".format(walletTotalClean, account['currency'])
	content = header + date + walletString + total

	#DISTRIBUTE
	if SMS:
		if len(account['phone']) > 7:
			if account['phoneEnabled'] == "True":
				sms.sendSMS(account['phone'], content)

	if EMAIL:
		if len(account['email']) > 5:
			if account['emailEnabled'] == "True":
				mail.mailsend(account['email'], header + walletTotalClean, content)

	print(content)

	#add wallet total to running total
	contentTotal += content + "\n"

summary = contentTotal + "Grand Total: {} {}".format(tools.prettyOutput(walletsTotal), base_currency)
print(summary)

#SEND SUMMARY
if EMAIL or SMS:
	try:
		mail.mailsend('juaney.garcia@gmail.com', 'Crypto {}'.format(datetime.date.today()), summary)
	except:
		print('Failed to send summary')
