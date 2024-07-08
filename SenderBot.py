from web3 import Web3
import time
import random

def check_balance(shm, address):
    checksum_address = shm.to_checksum_address(address)
    balance_wei = shm.eth.get_balance(checksum_address)
    return shm.from_wei(balance_wei, 'ether')

def send_transaction(shm, from_address, private_key, to_address, value_in_wei):
    to_address_checksum = None 
    while True:
        try:
            from_address_checksum = shm.to_checksum_address(from_address)
            to_address_checksum = shm.to_checksum_address(to_address)
            
            current_nonce = shm.eth.get_transaction_count(from_address_checksum, 'pending')
            transaction = {
                'to': to_address_checksum,
                'value': value_in_wei,
                'gas': 21000,
                'gasPrice': shm.to_wei('5', 'gwei'),
                'nonce': current_nonce,
            }

            signed_transaction = shm.eth.account.sign_transaction(transaction, private_key)

            transaction_hash = shm.eth.send_raw_transaction(signed_transaction.rawTransaction)
            print(f'###########################################################################')
            print(f'                                                                                            ')
            print(f'Current address: {from_address_checksum}, Saldo: {check_balance(shm, from_address_checksum)} SHM')
            print(f'Transaction sent! Address: {to_address_checksum}, Transaction Hash: {transaction_hash.hex()}')
            print(f'                                                                                            ')
            print(f'###########################################################################')
            break  

        except Exception as e:
            print(f'Error: {e}')
            print(f'{to_address_checksum}')
            print(f'I wait 2 minutes before trying again...')
            time.sleep(120)  


shm = Web3(Web3.HTTPProvider('https://sphinx.shardeum.org/'))

if shm.is_connected():
    print("You are connected to Shardeum Sphinx 1.X")

    with open('sender.txt', 'r') as file:
        lines = file.read().splitlines()
        account_address = lines[0].split('\t')[0]
        private_key = lines[0].split('\t')[1]

    with open('adresses.txt', 'r') as file:
        to_addresses = file.read().splitlines()

    while to_addresses:
        to_address = to_addresses[0]
        
        if to_address.lower() == 'the end':
            print("The end of the list has been reached.")
            break
        
        value_in_wei = shm.to_wei(16, 'ether')
        send_transaction(shm, account_address, private_key, to_address, value_in_wei)
        time.sleep(random.choice([38, 34, 35, 36]))  
        to_addresses = to_addresses[1:]  

else:
    print("Failed to connect to Shardeum Sphinx 1.X")
