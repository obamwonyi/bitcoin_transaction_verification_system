import os
import asyncio
from src.transaction import Transaction
from src.schema import TransactionSchema
from src.validation import validate_transactions
from src.mine import Mine

async def main() -> None:
    """
    This will be responsible for kick-starting the mining process
    :return: None
    """
    # Read and deserialize transactions from mempool directory
    transactions = []
    for filename in os.listdir("mempool"):
        filepath = os.path.join("mempool", filename)
        with open(filepath, "r") as file:
            json_data = file.read()
            transaction_schema = TransactionSchema()
            try:
                transaction = transaction_schema.load(json_data)
                transactions.append(transaction)
            except Exception as e:
                print(f"Error deserializing transaction {filename}: {e}")
        
    # Validate transactions asynchronously
    valid_transactions = await validate_transactions(transactions)

    # Mine the block
    block_data = mine_block(valid_transactions)

    with open("output.txt", "w") as output_file:
        output_file.write(block_data)


if __name__ == "__main__":
    asyncio.run(main())
