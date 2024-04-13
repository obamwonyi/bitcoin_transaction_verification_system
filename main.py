import os
import asyncio
# TODO: replace json with a serializer
import json
from src.transaction import Transaction, TransactionSchema
from src.validation import validate_transactions
from marshmallow import ValidationError
from src.mine import Mine

async def main():
    # Step 1: Read and deserialize transactions from the mempool directory
    transactions = []
    errors = 0
    for filename in os.listdir("mempool"):
        filepath = os.path.join("mempool", filename)
        with open(filepath, "r") as file:
            json_data = file.read()
            # TODO: This would be reimplemented after I fix deserizlizing with marshmallow
            transaction_schema = TransactionSchema()
            try:
                transaction = transaction_schema.load(json.loads(json_data))
                transactions.append(transaction)
                print(f"Deserialized transaction from {filename}")
            except ValidationError as e:
                errors = errors + 1
                print(f"Error deserializing transaction {filename}:")
                print(e.messages)

    print(f"Total transactions deserialized: {len(transactions)}")
    print(f"Total failed transactions:{errors}")

    # Step 2: Validate transactions asynchronously
    valid_transactions = await validate_transactions(transactions)

    # Step 3: Mine the block
    block_data = mine_block(valid_transactions)

    # Step 4: Write the block data to the output.txt file
    with open("output.txt", "w") as output_file:
        output_file.write(block_data)

if __name__ == "__main__":
    asyncio.run(main())
