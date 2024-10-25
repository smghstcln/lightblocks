import csv
import os
from web3 import Web3
from datetime import datetime, timezone


# Function to create CSV files
def initialize_csv_file(data_folder, csv_file_path):
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    with open(csv_file_path, mode='w', newline='', buffering=1) as file:
        writer = csv.writer(file)
        writer.writerow([
            'Transaction Hash',
            'Block Number',
            'Timestamp',
            'Gas Price (Gwei)',
            'Gas Used',
            'Number of Inputs',
            'Max Merkle Tree Depth'
        ])


# Function to get block number by timestamp
def get_block_by_timestamp(w3, timestamp):
    latest_block = w3.eth.get_block('latest')
    latest_block_number = latest_block.number
    latest_block_timestamp = latest_block.timestamp

    earliest_block_number = 0
    earliest_block_timestamp = w3.eth.get_block(earliest_block_number).timestamp

    if timestamp < earliest_block_timestamp:
        return earliest_block_number
    if timestamp > latest_block_timestamp:
        return latest_block_number

    # Binary search
    while earliest_block_number <= latest_block_number:
        mid_block_number = (earliest_block_number + latest_block_number) // 2
        mid_block = w3.eth.get_block(mid_block_number)
        mid_block_timestamp = mid_block.timestamp

        if mid_block_timestamp < timestamp:
            earliest_block_number = mid_block_number + 1
        elif mid_block_timestamp > timestamp:
            latest_block_number = mid_block_number - 1
        else:
            return mid_block_number

    return earliest_block_number


# Function to fetch logs in batches to avoid RPC-overload 
def fetch_logs_in_batches(w3, start_block, end_block, address, batch_size):
    logs = []
    for block_start in range(start_block, end_block + 1, batch_size):
        block_end = min(block_start + batch_size - 1, end_block)
        try:
            batch_logs = w3.eth.get_logs({
                'fromBlock': block_start,
                'toBlock': block_end,
                'address': address
            })
            logs.extend(batch_logs)
            print(f"Fetched logs from blocks {block_start} to {block_end}, total logs so far: {len(logs)}")
        except Exception as e:
            print(f"Error fetching logs from blocks {block_start} to {block_end}: {e}")
            continue 
    return logs



# Main function to collect transaction data
def collect_data(tz,start_date_str,end_date_str, data_folder, csv_file_path, w3, contract_address, batch_size, contract):
    # Initialize the CSV file
    initialize_csv_file(data_folder, csv_file_path)

    # Parse the dates and localize to Israeli time
    start_datetime = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
    start_datetime = tz.localize(start_datetime)

    end_datetime = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')
    end_datetime = tz.localize(end_datetime)

    # Convert to UTC timestamps
    start_timestamp = int(start_datetime.astimezone(timezone.utc).timestamp())
    end_timestamp = int(end_datetime.astimezone(timezone.utc).timestamp())

    # Get the corresponding block numbers
    print("Getting start block...")
    start_block = get_block_by_timestamp(w3, start_timestamp)
    print(f"Start block: {start_block}")

    print("Getting end block...")
    end_block = get_block_by_timestamp(w3, end_timestamp)
    print(f"End block: {end_block}")

    # Fetch logs related to the contract within the block range
    print("Fetching transaction hashes from logs...")
    try:
        logs = fetch_logs_in_batches(w3, start_block, end_block, contract_address, batch_size)
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return

    print(f"Total logs fetched: {len(logs)}")

    # Extract transaction hashes
    tx_hashes = set()
    for log in logs:
        tx_hashes.add(log['transactionHash'])

    print(f"Total unique transactions: {len(tx_hashes)}")

    # Initialize counters to locate potential errors
    total_transactions = len(tx_hashes)
    transactions_written = 0
    transactions_skipped_timestamp = 0
    transactions_skipped_function = 0
    transactions_skipped_exception = 0

    # Process transactions
    with open(csv_file_path, mode='a', newline='', buffering=1) as file:
        writer = csv.writer(file)

        for i, tx_hash in enumerate(tx_hashes, start=1):
            try:
                tx = w3.eth.get_transaction(tx_hash)
                tx_receipt = w3.eth.get_transaction_receipt(tx_hash)

                # Filter transactions by timestamp
                tx_block = w3.eth.get_block(tx.blockNumber)
                tx_timestamp = tx_block.timestamp
                if tx_timestamp < start_timestamp or tx_timestamp > end_timestamp:
                    print(f"Skipping transaction {tx_hash.hex()} due to timestamp")
                    transactions_skipped_timestamp += 1
                    continue

                # Check if the transaction is to our contract
                if tx.to and tx.to.lower() == contract_address.lower():
                    # Decode the transaction input
                    func_obj, func_args = contract.decode_function_input(tx.input)

                    if func_obj.fn_name == 'updatePriceFeeds':
                        # Extract the number of inputs
                        inputs = func_args['inputs']
                        number_of_inputs = len(inputs)

                        # Get the length of 'proof' array per input
                        merkle_tree_depths = [len(input_item['proof']) for input_item in inputs]
                        max_merkle_tree_depth = max(merkle_tree_depths) if merkle_tree_depths else 0

                        gas_used = tx_receipt.gasUsed
                        gas_price = tx.gasPrice  # In Wei
                        gas_price_gwei = Web3.from_wei(gas_price, 'gwei') 
                        block_number = tx.blockNumber

                        # Write data to CSV
                        writer.writerow([
                            tx_hash.hex(),
                            block_number,
                            tx_timestamp,
                            gas_price_gwei,
                            gas_used,
                            number_of_inputs,
                            max_merkle_tree_depth
                        ])
                        transactions_written += 1
                    else:
                        print(f"Skipping transaction {tx_hash.hex()} because function called is {func_obj.fn_name}")
                        transactions_skipped_function += 1
                else:
                    print(f"Skipping transaction {tx_hash.hex()} because 'to' address does not match contract address")
                    transactions_skipped_function += 1
            except Exception as e:
                print(f"Error processing transaction {tx_hash.hex()}: {e}")
                transactions_skipped_exception += 1
                continue  

    print(f"Total transactions processed: {total_transactions}")
    print(f"Total transactions written to CSV: {transactions_written}")
    print(f"Transactions skipped due to timestamp: {transactions_skipped_timestamp}")
    print(f"Transactions skipped due to function mismatch: {transactions_skipped_function}")
    print(f"Transactions skipped due to exceptions: {transactions_skipped_exception}")
    print("Data collection completed.")
