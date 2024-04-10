import asyncio

async def validate_transaction(transaction) -> bool:
    """
    This function is responsible for validating a
    transaction
    :param transaction: a transaction to be validated
    :return: bool
    """
    pass

async def validate_transactions(transactions) -> list:
    """
    gather and return all valid transactions
    :param transactions: all transactions, both valid and invalid
    :return: list
    """
    async_tasks = []
    for tx in transactions:
        async_task = validate_transaction(tx)
        async_tasks.append(async_task)

    validation_results = await asyncio.gather(*async_tasks)

    valid_transactions = []
    # Check and store valid transactions
    for tx, is_valid in zip(transactions, validation_results):
        if is_valid:
            valid_transactions.append(tx)

    return valid_transactions
