import random
import os
import requests

# Your API key
API_KEY = 'x'

def generate_private_key():
    return ''.join(random.choice('0123456789abcdef') for _ in range(64))

def check_balance(private_key):
    eth_balance = get_eth_balance(private_key)
    return eth_balance

def get_eth_balance(private_key):
    address = private_key_to_address(private_key, currency='ETH')
    url = f'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return int(data.get('result', 0)) / 1e18

def private_key_to_address(private_key, currency='ETH', eth_balance=0):
    if currency == 'ETH':
        address = '0x12345EthereumAddress'
        if eth_balance > 0:
            file_path = os.path.join(os.path.dirname(__file__), 'eth_non_zero_balance_private_keys.txt')
            with open(file_path, 'a') as eth_file:
                eth_file.write(private_key + '\n')
        return address

def main():
    while True:
        private_key = generate_private_key()
        eth_balance = check_balance(private_key)
        private_key_to_address(private_key, eth_balance=eth_balance)  # Pass eth_balance here
        print(f"Private Key: {private_key}, ETH Balance: {eth_balance}")

if __name__ == "__main__":
    main()
