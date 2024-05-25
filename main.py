import os
import asyncio
# TODO: replace json with a serializer
import json
from src.validation import ValidateTransaction
from src.mine import mine_block
from collections import defaultdict

async def main():
    """
    This function is the entry point of the entire project
    the overview of the functionality is commented in steps
    with an appropriate implementation of the concept of separation of concern
    in the form of modules.
    :return:
    """
    # Step 1: Read and deserialize transactions from the mempool directory
    transactions = []
    for filename in os.listdir("mempool"):
        filepath = os.path.join("mempool", filename)
        with open(filepath, "r") as file:
            json_data = file.read()
            try:
                loaded_data = json.loads(json_data)
                transactions.append(loaded_data)
            except:
                print(f"Error deserializing transaction {filename}:")

    # Step 2: Validate transactions asynchronously
    validate_transaction = ValidateTransaction()
    valid_transactions = await validate_transaction.validate_transactions(transactions)

    # Step 3: Mine the block
    block_data = mine_block(valid_transactions)

    # Step 4: Write the block data to the output.txt file
    with open("output.txt", "w") as output_file:
        output_file.write(block_data)

if __name__ == "__main__":
    asyncio.run(main())
