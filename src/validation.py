import asyncio
from typing import Any, List, Tuple, Union
from ecdsa import VerifyingKey, BadDigestError, SECP256k1
import hashlib
from .scripts import Scripts

# Todo: Remove the comment below
# anothter name for pubkey script is scriptpubkey


class ValidateTransaction:
    """
    Summary: This class is responsible for validating a bitcoin transaction asynchronously

    Attributes:

    Methods:
        validate_transaction(tx): validate individual transactions asynchronously
        validate_transactions(self, transactions): pass a transaction at a time for validation and gather and return
        all valid transactions

    """
    async def validate_transaction(self, tx: dict) -> Union[bool, dict, tuple]:
        """
        This static method is responsible for validating each transaction asynchronously
        Args:
            tx (dict): The transaction to be verified
        Returns:
            Union[bool, dict] : Either returns a bool (False) for an invalid transaction
            or returns the transaction that is valid
        """
        # Todo: Step 1 : Validate P2PKH
        scripts = Scripts()
        if not await scripts.validate_p2pkh_script(tx):
            print("Failed P2PKH")
            return False, "The p2pkh script validation failed"

        print("Passed P2PKH")
        return True

    async def validate_transactions(self, transactions: List[Any]) -> Tuple[Any, ...]:
        """
        Validates and gathers all valid transactions that would later be mined. Then return
        The gathered transactions as a tuple
        Args:
            transactions (List[Any]) : A list of all the transactions with any form of data in it.
        Returns:
            Tuple[Any]: Tuple of all the valid transactions
        Raises:
            TODO: description of exceptions, if any
        """
        tasks = [self.validate_transaction(transaction) for transaction in transactions]
        return await asyncio.gather(*tasks)
