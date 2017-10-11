#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import wallets
import cryptos
import datetime
import sys
import forex
import tools

#Global Variables
today = datetime.date.today()
SMS = False
EMAIL = False

#Set runtime variables
if len(sys.argv) > 1:
	for arg in sys.argv:
		if arg == "sms":
			import sms
			SMS = True
		if arg == "email":
			import mail
			EMAIL = True

try:
	base_currency = json.loads(open('settings.json', 'r').read())['Base_currency']
except:
	print("Failed to load base currency from settings.json defaulting to USD")
	base_currency = 'USD'
	
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
	contentTotal += content +"\n"

summary = contentTotal + "Grand Total: {} {}".format(tools.prettyOutput(walletsTotal), base_currency)
print(summary)

if EMAIL:
	try:
		from_mail = json.loads(open('settings.json', 'r').read())['Email_FROMEMAIL']
		sendEmail(from_mail, walletsTotal, summary)
	except:
		print('Failed to send summary')