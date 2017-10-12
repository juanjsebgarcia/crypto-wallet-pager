# CryptoWalletPager
Easily schedule updates for the fiat value of your Ethereum wallets including tokens.

Built in support for email and SMS through Twilio.

For help tweet @juanjsebgarcia or use github

## Installation
The application is designed to run on Python3
1. Clone the repo to local storage
2. Run: pip install -r requirements.txt
3. Rename example_accounts.json to accounts.json
4. Rename example_settings.json to settings.json
5. Modify the file values as necessary

JSON mappings can be found later in this readme

# Scheduling the application
Scheduling can be achieved with a cronjob. Visit crontab-generator.org for assitance

Running the file outputs only to console. The email and sms flags are used to enable each feature.

SMS only 
>python deploy.py sms

Email & SMS
>python deploy.py email sms

Example cronjob to run at midday:
>00 12 * * * /usr/bin/python3 /home/ubuntu/CryptoWalletPager/deploy.py sms email

## API Keys
You will need to obtain a free key from Etherscan.io this can be placed in the settings.py

SMS support requires keys from twilio.com

## SMS support
SMS support is handled by Twilio. You can enter your account settings in settings.py

## Email support
Emails are sent via SMTP. You can enter your email settings in settings.py

# Accounts.json
The JSON for an account is as follows:

"name": A chosen name for the wallet

"email": Email of wallet owner

"emailEnabled": Boolean toggle to enable or disable emails

"phone": Phone number of owner with country prefix

"phoneEnabled": Boolean toggle to enable or disable SMS

"currency": Code representing target output fiat (GBP, USD, CNY etc)

"wallet": 0x wallet addresss

"tokens": Comma seperated list of all tokens to check for

# Settings.json

The JSON for the settings is as follows:

"Etherscan_api": Etherscan API key from etherscan.io

"Twilio_account_sid": SID token provided by Twilio

"Twilio_auth_token": API Auth token provided by Twilio

"Twilio_source_number": Number provided by Twilio

"Email_SMTPSERVER": Server address for the SMTP service

"Email_USERNAME": Username for the SMTP service

"Email_PASSWORD": Password for the SMTP service

"Email_FROMEMAIL": From email for the SMTP service

"Base_currency": Fallback default currency code

## Data Sources
Ethereum wallet data provided by Etherscan.io

Token wallet data provided by tokenbalance.com

Crypto values provided by coincap.io

Forex rates data provided by fixer.io

Token:Contract mappings taken from MyEtherWallet.com