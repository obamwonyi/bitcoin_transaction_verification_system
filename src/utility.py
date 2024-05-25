import asyncio
from typing import Any, List, Tuple, Union
from ecdsa import VerifyingKey, BadDigestError, SECP256k1
import hashlib

class Utility:
    """
    Summary: This class will be responsible for holding methods that acts as aid for some execution process
    in the program implementation.

    Attributes:

    Methods:
        validate_transaction(tx): validate individual transactions asynchronously
        validate_transactions(self, transactions): pass a transaction at a time for validation and gather and return
        all valid transactions
    """

    def extract_pubkey_hash(self, scriptpubkey: str) -> Union[str, Tuple[bool, str]]:
        """
        This method will extract the pubkey_hash from the pubkey_script pass
        Args:
            scriptpubkey (str): A string of random bytes
        Returns:
            str: string of the pubkey_hash
        """
        script_bytes = bytes.fromhex(scriptpubkey)
        if script_bytes[:3] != b'\x76\xa9\x14':
            return False, "Invalid scriptpubkey format for P2PKH output"

        pubkey_hash = script_bytes[3:23]
        return pubkey_hash.hex()


    def parse_signature_script(self, tx_input: dict) -> Union[Tuple[bytes, bytes], Tuple[bool, str]]:
        """
        Extract signature and public key from scriptsig or witness
        Args:
            tx_input (dict): Dictionary containing input data, including scriptsig and witness
        Returns:
            Union[Tuple[bytes, bytes], Tuple[bool, str]]: Tuple of the signature and public key if
            the extraction was successful, or tuple of False and string if the extraction failed
        """
        script_sig = tx_input.get("scriptsig", "")
        if not script_sig:
            return False, "No scriptSig provided"

        try:
            # Convert script_sig to bytes if it's not already
            if isinstance(script_sig, str):
                script_sig = bytes.fromhex(script_sig)
            # Get the length of the signature from the first byte
            sig_len = script_sig[0]

            # Extracting the signature based on its length
            signature = script_sig[1:sig_len + 1]

            # Get the length of the public key from the byte immediately after the signature
            pubkey_len = script_sig[sig_len + 1]

            # Extract the public key based on its length
            pubkey = script_sig[sig_len + 2:sig_len + 2 + pubkey_len]

            # print(f"Decoded signature: {signature.hex()}")
            # print(f"Decoded public key: {pubkey.hex()}")

            return signature, pubkey

        except Exception as e:
            return False, f"Error parsing scriptSig: {str(e)}"

    def verify_signature(self, signature: str, pubkey: str, tx: dict) -> bool:
        """
        Verify the signature of a transaction with the aid of the pubkey and the
        signature passed
        Args:
            signature (str): string of bytes that represents the signature of the transaction
            pubkey (str): string of bytes for the pubkey
            tx (dic): dictionary of data, like other transaction.
        Returns:
            bool: False if the signature is invalid and True if the signature is valid
        """
        try:
            verifying_key = VerifyingKey.from_string(bytes.fromhex(pubkey), curve=SECP256k1)
            # Encodes transactions in bytes
            tx_bytes = tx.encode()
            # Hash the transaction once
            sha256_hash_1 = hashlib.sha256(tx_bytes).digest()
            # Hash the transaction for the second time.
            sha256_hash_2 = hashlib.sha256(sha256_hash_1).digest()
            message_digest = sha256_hash_2
            # Verify the transaction
            verifying_key.verify(bytes.fromhex(signature), message_digest, hashlib.sha256)

            return True
        except BadDigestError:
            return False

        return False

    def hash160(data: bytes) -> bytes:
        """
        Perform SHA-256 followed by RIPEMD-160
        Args:
             data (bytes) : byte data to be hashed to hash160
        Returns:
            bytes : the hased data in form of bytes
        """
        sha256_hash = hashlib.sha256(data).digest()
        return hashlib.new('ripemd160', sha256_hash).digest()