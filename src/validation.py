import asyncio



class ValidateTransaction:

    async def validate_transaction(self, tx) -> (bool, str):
        """
        :param tx:
        :return: validated transaction
        """
        return True


    async def validate_transactions(self, transactions):
        """
        Validates and gathers all valid transactions that would later be mined.
        :param transactions:
        :return:
        """
        tasks = [self.validate_transaction(transaction) for transaction in transactions]
        return await asyncio.gather(*tasks)