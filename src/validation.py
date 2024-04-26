import asyncio

from bitcoin.core import MAX_BLOCK_SIZE
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from typing import Tuple
from bitcoinlib.transactions import Transaction as BitcoinTransaction

async def validate_transaction(transaction) -> Tuple[bool, str]:
    """
    Validate a single transaction.
    :param transaction: The transaction to validate.
    :return: A tuple containing a boolean indicating whether the transaction is valid, and a string message.
    """
    # Check if the transaction has inputs and outputs
    if not transaction.vin:
        return False, "Transaction has no inputs"
    if not transaction.vout:
        return False, "Transaction has no outputs"

    # Initialize the total input and output values
    total_input_value = 0
    total_output_value = 0
    # Iterate over the inputs
    for tx_input in transaction.vin:
        # Handle coinbase transactions separately
        if tx_input.is_coinbase:
            # Coinbase transactions have specific rules that need to be validated
            # Check if the coinbase transaction follows the correct format
            # and has a valid block height and coinbase value
            if not validate_coinbase_transaction(tx_input):
                return False, f"Invalid coinbase transaction input: {tx_input}"
        else:
            # Extract the public key from the input witness
            if not tx_input.witness:
                return False, f"Input {tx_input.txid}:{tx_input.vout} has no witness"

            public_key_bytes = bytes.fromhex(tx_input.witness[-1])

            # Construct the public key object
            public_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256K1(), public_key_bytes)

            # Extract the signature from the input witness
            signature_bytes = b"".join(bytes.fromhex(witness_item) for witness_item in tx_input.witness[:-1])

            # Get the transaction data that was signed for this input
            tx_input_data = get_tx_input_data(transaction, tx_input)

            # Define the signature algorithm
            signature_algorithm = ec.EllipticCurveSignatureAlgorithm(hashes.SHA256())

            try:
                # Verify the signature using the public key, signature, and transaction data
                public_key.verify(
                    signature_bytes,
                    tx_input_data,
                    signature_algorithm
                )
            except InvalidSignature:
                return False, f"Invalid signature for input {tx_input.txid}:{tx_input.vout}"

            # Add the input value to the total input value
            total_input_value += tx_input.prevout.value

            # Validate the input script
            try:
                bitcoin_tx = BitcoinTransaction.from_dict(transaction)
                bitcoin_tx.verify_input_signature(tx_input.vout)
            except Exception as e:
                return False, f"Invalid input script for {tx_input.txid}:{tx_input.vout}: {str(e)}"

    # Iterate over the outputs
    for tx_output in transaction.vout:
        # Add the output value to the total output value
        total_output_value += tx_output.value

        # Validate the output script
        try:
            bitcoin_tx = BitcoinTransaction.from_dict(transaction)
            bitcoin_tx.verify_output_script(tx_output.scriptpubkey_asm)
        except Exception as e:
            return False, f"Invalid output script: {str(e)}"

    # Check if the total input value is greater than or equal to the total output value
    if total_input_value < total_output_value:
        return False, "Total input value is less than total output value"

    # Calculate the transaction fee
    transaction_fee = total_input_value - total_output_value

    # Validate transaction fee according to the fee rules
    if transaction_fee < 0:
        return False, "Transaction fee cannot be negative"

    # Check if the transaction size exceeds the maximum block size
    transaction_size = sum(len(tx_input.scriptsig) for tx_input in transaction.vin) + \
                       sum(len(tx_output.scriptpubkey) for tx_output in transaction.vout)
    if transaction_size > MAX_BLOCK_SIZE:
        return False, "Transaction size exceeds the maximum block size"

    return True, "Transaction is valid"

def validate_coinbase_transaction(tx_input) -> bool:
    """
    Validate a coinbase transaction input.
    :param tx_input: The coinbase transaction input to validate.
    :return: True if the coinbase transaction input is valid, False otherwise.
    """
    # Implement your coinbase transaction validation logic here
    # For example, you could check if the block height and coinbase value are valid
    # based on the current network rules and block subsidies.
    # This is just a placeholder function, you need to implement the actual validation logic.
    return True

async def validate_transactions(transactions) -> list:
    """
    Validate a list of transactions asynchronously.
    :param transactions: A list of transactions to validate.
    :return: A list of valid transactions.
    """
    async_tasks = [validate_transaction(tx) for tx in transactions]

    try:
        validation_results = await asyncio.gather(*async_tasks)
    except Exception as e:
        print(f"An error occurred during transaction validation, Error: {e}")
        return []

    valid_transactions = [tx for tx, (is_valid, _) in zip(transactions, validation_results) if is_valid]

    return valid_transactions

def get_tx_input_data(transaction, tx_input):
    """
    Helper function to construct the transaction data that was signed for a given input.
    This implementation assumes the transaction version is 1 or higher.
    """
    tx_data = b""
    tx_data += transaction.version.to_bytes(4, byteorder="little")
    tx_data += tx_input.prevout.scriptpubkey.encode()
    tx_data += tx_input.prevout.value.to_bytes(8, byteorder="little")
    tx_data += tx_input.sequence.to_bytes(4, byteorder="little")
    tx_data += transaction.locktime.to_bytes(4, byteorder="little")

    return tx_data