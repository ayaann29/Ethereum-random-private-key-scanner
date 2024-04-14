This code generates random hexadecimal private keys and sends it to ethereum network to check for non zero balance. 
If any private key with non zero balance is found (very unlikely), this code makes a new txt file on the same path of code which has the private key with its balance, which can be used to import wallet.  
This code displays live progress of private key scanning along with corresponding eth balance on the python window.

requirements- 
1. pip install aiohttp
2. etherscan api key (free api key is available on etherscan.io) replace 'x' on line 7 of "eth random key scan main.py"

The free api key provided by etherscan has a limit of 5 calls per ip per second, so i have modified this code to match this limit.
Just replace 'x' on line 7 of "eth random key scan main.py" with your api key and private key scanner

This code is designed for educational purposes, with the sole intention of brute forcing inactive wallets.
