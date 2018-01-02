#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
import sys

from modules import bitcoin
from modules import forex
from modules import web3
from modules import tools

from notifications import mail

#Global Variables
today = datetime.date.today()
SMS = False
EMAIL = False

#Set runtime variables
if len(sys.argv) > 1:
	for arg in sys.argv:
		if arg == "sms":
			SMS = True
			from notifications import sms
		if arg == "email":
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
content_total = ""
wallets_total = 0

#FOR EACH ACCOUNT
for account in accounts:
	#Track fiat balance in each wallet
	wallet_balance = 0
	wallet_string = ""

	#ETHEREUM
	if account['wallet'] is not None or account['wallet'] != '':
		eth_balance = web3.get_eth_balance(account['wallet'])
		eth_usd_value = forex.get_usd_value('ETH')*eth_balance
		eth_local_value = forex.from_usd(account['currency'], eth_usd_value)
		if eth_local_value > 0:
			wallet_balance += eth_local_value
			wallet_string += "ETH: ~{} {}\n".format(tools.pretty_output(eth_local_value), account['currency'])
			wallets_total += eth_usd_value

		#ERC20 TOKENS
		contracts = web3.load_contracts()
		for token in contracts:
			token_abi = web3.make_abi_call(token['address'])
			token_balance = web3.get_token_balance(token['decimal'], token_abi, account['wallet'])
			token_usd_value = forex.get_usd_value(token['symbol'])*token_balance
			token_local_value = forex.from_usd(account['currency'], token_usd_value)
			if token_local_value > 0:
				wallet_balance += token_local_value
				wallet_string += "{}: ~{} {}\n".format(str(token['symbol']), tools.pretty_output(token_local_value), account['currency'])
				wallets_total += token_usd_value

		#bitcoin
		if account['bitcoin'] is not None or account['bitcoin'] != '':
			bitcoin_addresses = account['bitcoin'].split(",")
			for address in bitcoin_addresses:
					balance = bitcoin.get_bitcoin_balance(address)
					bitcoin_usd_value = forex.get_usd_value('BTC')*balance
					bitcoin_local_value += forex.from_usd(account['currency'], bitcoin_usd_value)
			if bitcoin_local_value > 0:
				wallet_balance += bitcoin_local_value
				wallet_string += "{}: ~{} {}\n".format('BTC', tools.prettyOutput(bitcoin_local_value), account['currency'])
				wallets_total += bitcoin_usd_value


	#PREPARE EXPORT CONTENT
	wallet_total_clean = tools.pretty_output(wallet_balance)
	header = account['name'] +" Crypto Wallet\n"
	date =  "{:%d %b %Y}".format(today)+"\n"
	total = "TOTAL: ~{} {}".format(wallet_total_clean, account['currency'])
	content = header + date + wallet_string + total

	#DISTRIBUTE
	if SMS:
		if len(account['phone']) > 7:
			if account['phoneEnabled'] == "True":
				sms.send_sms(account['phone'], content)

	if EMAIL:
		if len(account['email']) > 5:
			if account['emailEnabled'] == "True":
				mail.mail_send(account['email'], header + wallet_balance, content)

	print(content)

	#add wallet total to running total
	content_total += content + "\n"

summary = content_total + "Grand Total: {} {}".format(tools.prettyOutput(wallets_total), base_currency)
print(summary)

#SEND SUMMARY
if EMAIL or SMS:
	try:
		admin_email = json.loads(open('settings.json', 'r').read())['Email_FROMEMAIL']
		mail.mailsend(admin_email, 'Crypto {}'.format(datetime.date.today()), summary)
	except:
		print('Failed to send summary')
