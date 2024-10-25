import os
from web3 import Web3
import json
import pytz
from web3.middleware import ExtraDataToPOAMiddleware
from utils import collect_data

# RPC URL Scroll
scroll_rpc_url = 'https://rpc.scroll.io'

# Initialize web3 instance
w3 = Web3(Web3.HTTPProvider(scroll_rpc_url))

# Inject compatibility middleware to handle extradata
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

# Contract address of the proxy contract
contract_address = '0x1f8c6f1f224fe730421f51da9bd5efd75986a08f'

# Contract to checksum format
contract_address = w3.to_checksum_address(contract_address)

# Implementation contract ABI
implementation_abi_json = '''[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"caller","type":"address"}],"name":"CallerIsNotWhitelisted","type":"error"},{"inputs":[{"internalType":"uint16","name":"feedId","type":"uint16"}],"name":"FeedNotSupported","type":"error"},{"inputs":[],"name":"InvalidAddress","type":"error"},{"inputs":[],"name":"InvalidInitialization","type":"error"},{"inputs":[],"name":"InvalidInput","type":"error"},{"inputs":[],"name":"MissingLeafInputs","type":"error"},{"inputs":[],"name":"NotInitializing","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"OwnableInvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"OwnableUnauthorizedAccount","type":"error"},{"inputs":[{"internalType":"uint16","name":"feedId","type":"uint16"}],"name":"SymbolReplay","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint16","name":"feedId","type":"uint16"},{"indexed":false,"internalType":"uint256","name":"rate","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"}],"name":"RateUpdated","type":"event"},{"inputs":[],"name":"getFeedVerifier","outputs":[{"internalType":"contract IEOFeedVerifier","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"feedId","type":"uint16"}],"name":"getLatestPriceFeed","outputs":[{"components":[{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"timestamp","type":"uint256"},{"internalType":"uint256","name":"eoracleBlockNumber","type":"uint256"}],"internalType":"struct IEOFeedManager.PriceFeed","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16[]","name":"feedIds","type":"uint16[]"}],"name":"getLatestPriceFeeds","outputs":[{"components":[{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"timestamp","type":"uint256"},{"internalType":"uint256","name":"eoracleBlockNumber","type":"uint256"}],"internalType":"struct IEOFeedManager.PriceFeed[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"feedVerifier","type":"address"},{"internalType":"address","name":"owner","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"feedId","type":"uint16"}],"name":"isSupportedFeed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"publisher","type":"address"}],"name":"isWhitelistedPublisher","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"feedVerifier","type":"address"}],"name":"setFeedVerifier","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16[]","name":"feedIds","type":"uint16[]"},{"internalType":"bool[]","name":"isSupported","type":"bool[]"}],"name":"setSupportedFeeds","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"leafIndex","type":"uint256"},{"internalType":"bytes","name":"unhashedLeaf","type":"bytes"},{"internalType":"bytes32[]","name":"proof","type":"bytes32[]"}],"internalType":"struct IEOFeedVerifier.LeafInput","name":"input","type":"tuple"},{"components":[{"internalType":"uint256","name":"epoch","type":"uint256"},{"internalType":"uint256","name":"blockNumber","type":"uint256"},{"internalType":"bytes32","name":"eventRoot","type":"bytes32"},{"internalType":"bytes32","name":"blockHash","type":"bytes32"},{"internalType":"uint256","name":"blockRound","type":"uint256"}],"internalType":"struct IEOFeedVerifier.Checkpoint","name":"checkpoint","type":"tuple"},{"internalType":"uint256[2]","name":"signature","type":"uint256[2]"},{"internalType":"bytes","name":"bitmap","type":"bytes"}],"name":"updatePriceFeed","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"leafIndex","type":"uint256"},{"internalType":"bytes","name":"unhashedLeaf","type":"bytes"},{"internalType":"bytes32[]","name":"proof","type":"bytes32[]"}],"internalType":"struct IEOFeedVerifier.LeafInput[]","name":"inputs","type":"tuple[]"},{"components":[{"internalType":"uint256","name":"epoch","type":"uint256"},{"internalType":"uint256","name":"blockNumber","type":"uint256"},{"internalType":"bytes32","name":"eventRoot","type":"bytes32"},{"internalType":"bytes32","name":"blockHash","type":"bytes32"},{"internalType":"uint256","name":"blockRound","type":"uint256"}],"internalType":"struct IEOFeedVerifier.Checkpoint","name":"checkpoint","type":"tuple"},{"internalType":"uint256[2]","name":"signature","type":"uint256[2]"},{"internalType":"bytes","name":"bitmap","type":"bytes"}],"name":"updatePriceFeeds","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"publishers","type":"address[]"},{"internalType":"bool[]","name":"isWhitelisted","type":"bool[]"}],"name":"whitelistPublishers","outputs":[],"stateMutability":"nonpayable","type":"function"}]''' 

# Parse ABI
implementation_abi = json.loads(implementation_abi_json)

# Create the contract object at the proxy address with the implementation ABI
contract = w3.eth.contract(address=contract_address, abi=implementation_abi)

# Data storage path
data_folder = 'data'
csv_file_path = os.path.join(data_folder, 'scroll_data.csv')

# Define batch size to fetch transaction logs
batch_size=10000

# Define time range settings
tz = pytz.timezone('Israel')            # Time zone
start_date_str = '2024-9-20 12:00:00'   # Start date and time
end_date_str = '2024-10-20 12:00:00'    # End date and time

# Collect the data
collect_data(tz,start_date_str,end_date_str, data_folder, csv_file_path, w3, contract_address, batch_size, contract)

