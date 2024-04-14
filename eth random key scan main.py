import os
import requests
import asyncio
import aiohttp
import random

API_KEY = 'x'
CONCURRENT_REQUESTS = 5

async def generate_private_key():
    return ''.join(random.choice('0123456789abcdef') for _ in range(64))

async def check_balance(private_key):
    async with aiohttp.ClientSession() as session:
        eth_balance = await get_eth_balance(session, private_key)
        return eth_balance

async def get_eth_balance(session, private_key):
    address = private_key_to_address(private_key, currency='ETH')
    url = f'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={API_KEY}'
    async with session.get(url) as response:
        try:
            data = await response.json()
            return int(data.get('result', 0)) / 1e18
        except aiohttp.client_exceptions.ContentTypeError as e:
            print("ContentTypeError:", e)
            await save_failed_response(await response.text())
            return 0

def private_key_to_address(private_key, currency='ETH'):
    if currency == 'ETH':
        return '0x12345EthereumAddress'

async def save_private_key(private_key, eth_balance):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_dir, 'checked_private_keys.txt'), 'a') as file:
        file.write(f"Private Key: {private_key}\n")
        file.write(f"ETH Balance: {eth_balance}\n\n")
    if eth_balance > 0:
        with open(os.path.join(script_dir, 'eth_non_zero_balance_private_keys.txt'), 'a') as eth_file:
            eth_file.write(private_key + '\n')

async def save_failed_response(response_text):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_dir, 'failed_response.json'), 'w') as file:
        file.write(response_text)

async def main():
    while True:
        tasks = []
        for _ in range(CONCURRENT_REQUESTS):
            private_key = await generate_private_key()
            task = asyncio.create_task(check_and_save(private_key))
            tasks.append(task)
        await asyncio.gather(*tasks)

async def check_and_save(private_key):
    eth_balance = await check_balance(private_key)
    await save_private_key(private_key, eth_balance)
    print(f"Private Key: {private_key}, ETH Balance: {eth_balance}")

if __name__ == "__main__":
    asyncio.run(main())
