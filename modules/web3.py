from web3 import Web3, HTTPProvider, IPCProvider
import json

token_contracts = None

def get_web3():
    '''
    Return web3 object
    '''
    project_id = json.loads(open('settings.json', 'r').read())['Infura_project_id']
    return Web3(HTTPProvider('https://mainnet.infura.io/v3/'+project_id))


def get_eth_balance(wallet):
    '''
    Returns ETH balance of a wallet
    '''
    web3 = get_web3()
    wei = web3.eth.getBalance(wallet)
    divisor = 10**18 #fixed divisor for Wei -> ETH
    return wei/divisor


def load_contracts():
	'''
	Loads contracts from MEW git, falls back to local instance if fails
	'''
	global token_contracts
	if token_contracts is None:
		try:
			contracts = requests.get('https://raw.githubusercontent.com/kvhnuke/etherwallet/mercury/app/scripts/tokens/ethTokens.json').json()
		except:
			file = open('ethTokens.json', 'r')
			contracts = json.loads(file.read())
	return contracts


def make_abi_call(contract_address):
    web3 = get_web3()
    # Generic ABI
    abi = json.loads('[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]')
    token = web3.eth.contract(contract_address, abi=abi)
    return token


def get_token_balance(decimal, token, wallet):
    try:
        divisor = 10**decimal
        return token.call().balanceOf(wallet) / divisor
    except:
        return token.call().balanceOf(wallet)
