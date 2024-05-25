import asyncio
from typing import Any, List, Tuple, Union
from ecdsa import VerifyingKey, BadDigestError, SECP256k1
import hashlib
from .utility import Utility

class Scripts:
    """
    Summary: This class contains the various scripts for validating a bitcoin transaction, the likes of
    P2PKH : Pay Too Public Key Hash
    P2WPKH : Pay Too Witness Public Key Hash


    Attributes:

    Methods:
        validate_p2pkh_script(self, tx: dict) : validates the transaction with Pay Too Public Key Hash(P2PKH)
    """

    async def validate_p2pkh_script(self, tx: dict) -> bool:
        """
        Adds to the transaction validation process by validating the scriptpubkey
        Args:
            tx (dict) : A dictionary representation of the json transaction format from mempool
        Returns:
            bool: False if the transaction is not valid
        """
        for tx_input in tx["vin"]:
            # list_of_script_types = ['v1_p2tr', 'v0_p2wpkh', 'p2sh', 'p2pkh', 'v0_p2wsh']
            referenced_output = tx_input["prevout"]
            scriptpubkey_type = referenced_output["scriptpubkey_type"]

            if scriptpubkey_type != "p2pkh" and scriptpubkey_type != "v0_p2wpkh":
                continue

            #
            if scriptpubkey_type == "p2pkh":
                utility = Utility()
                sig, pubkey = utility.parse_signature_script(tx_input)
                pubkey_script = referenced_output["scriptpubkey"]
                pubkey_hash = utility.extract_pubkey_hash(pubkey_script)

                stack = []
                stack.append(sig)
                stack.append(pubkey)
                for opcode in pubkey_script:
                    if opcode == "OP_DUP":
                        stack.append(stack[-1])
                    elif opcode == "OP_HASH160":
                        pubkey_hash_from_stack = utility.hash160(stack.pop())
                        stack.append(pubkey_hash_from_stack)
                    elif opcode == "OP_EQUALVERIFY":
                        top1, top2 = stack.pop(), stack.pop()
                        if top1 != top2:
                            return False
                    elif opcode == "OP_CHECKSIG":
                        pubkey = stack.pop()
                        sig = stack.pop()
                        if not utility.verify_signature(sig, pubkey, tx):
                            print("Faild P2PKH")
                            return False
                print("Passed P2PKH")
                return True

        return False