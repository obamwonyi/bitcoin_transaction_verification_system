import asyncio
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


def validate_transaction(transaction):
    # Check if the transaction has inputs and outputs
    if not transaction.vin:
        return False, "Transaction has no inputs"
    if not transaction.vout:
        return False, "Transaction has no outputs"

    # Iterate over the inputs
    for tx_input in transaction.vin:
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

    return True, "Transaction is valid"


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

    try:
        validation_results = await asyncio.gather(*async_tasks)
    except Exception as e:
        print(f"An error occurred during transaction validation, Error: {e}")
        return []

    valid_transactions = []
    # Check and store valid transactions
    for tx, is_valid in zip(transactions, validation_results):
        if is_valid:
            valid_transactions.append(tx)
    
    return valid_transactions
