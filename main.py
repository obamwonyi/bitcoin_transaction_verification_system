import os
import asyncio
# TODO: replace json with a serializer
import json
from src.transaction import Transaction, TransactionSchema
from src.validation import ValidateTransaction
from marshmallow import ValidationError
from src.mine import mine_block
from collections import defaultdict

TRANSACTION_BY_ID = defaultdict(dict)

# TODO: Remove
async def main():
    # Step 1: Read and deserialize transactions from the mempool directory
    transactions = []
    for filename in os.listdir("mempool"):
        filepath = os.path.join("mempool", filename)
        with open(filepath, "r") as file:
            json_data = file.read()
            transaction_schema = TransactionSchema()
            try:
                loaded_data = json.loads(json_data)
                transaction = transaction_schema.load(loaded_data)

                for tx_input in transaction.vin:
                    txid = tx_input["txid"]
                    if txid:
                        TRANSACTION_BY_ID[txid] = loaded_data

                transactions.append(loaded_data)
                # print(f"Deserialized transaction from {filename}")
            except ValidationError as e:
                # errors = errors + 1
                print(f"Error deserializing transaction {filename}:")
                print(e.messages)

    # print(f"Total transactions deserialized: {len(transactions)}")
    # print(f"Total failed transactions:{errors}")

    # Step 2: Validate transactions asynchronously
    # valid_transactions = await validate_transaction.validate_transactions(transactions)

    # implement an initial transaction validation process.

    # print(valid_transactions)

    # print(valid_transactions)
    # Step 3: Mine the block
    block_data = mine_block(valid_transactions)

    # Step 4: Write the block data to the output.txt file
    with open("output.txt", "w") as output_file:
        output_file.write(block_data)

if __name__ == "__main__":
    asyncio.run(main())
