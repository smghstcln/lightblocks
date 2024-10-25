import os
from web3 import Web3
import json
import pytz
from utils import collect_data

# RPC URL zkLINK
zklink_rpc_url = 'https://rpc.zklink.io'

# Initialize web3 instance 
w3 = Web3(Web3.HTTPProvider(zklink_rpc_url))

# Contract address of the proxy contract
contract_address = '0xEECECaecf142992c25668c925d6E2eEF3A8C0DCE'

# Convert address to checksum format
contract_address = w3.to_checksum_address(contract_address)

# Implementation contract ABI 
implementation_abi_json = '''[{"inputs": [{"components": [{"internalType": "uint256","name": "leafIndex","type": "uint256"},{"internalType": "bytes","name": "unhashedLeaf","type": "bytes"},{"internalType": "bytes32[]","name": "proof","type": "bytes32[]"}],"internalType": "struct IEOFeedVerifier.LeafInput[]","name": "inputs","type": "tuple[]"},{"components": [{"internalType": "uint256","name": "epoch","type": "uint256"},{"internalType": "uint256","name": "blockNumber","type": "uint256"},{"internalType": "bytes32","name": "eventRoot","type": "bytes32"},{"internalType": "bytes32","name": "blockHash","type": "bytes32"},{"internalType": "uint256","name": "blockRound","type": "uint256"}],"internalType": "struct IEOFeedVerifier.Checkpoint","name": "checkpoint","type": "tuple"},{"internalType": "uint256[2]","name": "signature","type": "uint256[2]"},{"internalType": "bytes","name": "bitmap","type": "bytes"}],"name": "updatePriceFeeds","outputs": [],"stateMutability": "nonpayable","type": "function"}]'''  

# Parse ABI
implementation_abi = json.loads(implementation_abi_json)

# Create the contract object at the proxy address with the implementation ABI
contract = w3.eth.contract(address=contract_address, abi=implementation_abi)

# Data storage path
data_folder = 'data'
csv_file_path = os.path.join(data_folder, 'zklink_data.csv')

# Define batch size to fetch transaction logs
batch_size=100000

# Define time range settings
tz = pytz.timezone('Israel')            # Time zone
start_date_str = '2024-9-20 12:00:00'   # Start date and time
end_date_str = '2024-10-20 12:00:00'    # End date and time

# Collect the data
collect_data(tz,start_date_str,end_date_str, data_folder, csv_file_path, w3, contract_address, batch_size, contract)

