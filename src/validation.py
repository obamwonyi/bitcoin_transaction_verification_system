import asyncio
import re
import time


class ValidateTransaction:

    def __init__(self, transaction_by_id):
        self.transaction_by_id = transaction_by_id

    def validate_transaction_version(self, tx) -> bool:
        """
        Validate the transaction version.
        :param tx:
        :return: Bool
        """
        if tx.get("version") == 1 or tx.get("version") == 2:
            return True
        return False

    async def retrieve_transaction(self, txid) -> dict:
        """
        Retrieve a transaction from its ID
        :param txid: Transaction ID
        :return: dictionary form of transaction
        """
        transaction = self.transaction_by_id.get(txid)
        if transaction:
            return transaction
        else:
            print(f"Transaction with txid {txid} not found")
            return None

    async def verify_input_script(self, prev_tx, vout, script_pubkey) -> bool:
        """
        Validates the scriptSig or witness.
        :param prev_tx: Previous transaction dictionary
        :param vout: Output index
        :param script_pubkey: ScriptPubKey to be verified
        :return: bool
        """
        prev_output = prev_tx["vout"][vout]
        return prev_output["scriptpubkey"] == script_pubkey

    async def is_valid_output_script(self, scriptpubkey):
        """
        Validate the script public key of the output
        :param scriptpubkey: The script public key to validate
        :return: True if the script public key is valid, False otherwise
        """
        # Define a regular expression pattern to match P2PKH script public keys
        p2pkh_pattern = r'^OP_DUP OP_HASH160 [0-9a-fA-F]{40} OP_EQUALVERIFY OP_CHECKSIG$'

        # Check if the script public key matches the P2PKH pattern
        if re.match(p2pkh_pattern, scriptpubkey):
            return True
        else:
            return False

    async def validate_transaction_amount(self, tx) -> bool:
        async def validate_transaction_amount(self, tx) -> bool:
            """
            Validates the transaction amount
            :param tx: The transaction to validate
            :return: True if the transaction amount is valid, False otherwise
            """
            total_input_value = 0
            total_output_value = 0

            # Calculate the total input value
            for tx_input in tx.get("vin", []):
                txid = tx_input.get("txid")
                vout = tx_input.get("vout")

                # Retrieve the previous transaction output
                prev_tx = await self.retrieve_transaction(txid)
                if prev_tx is None:
                    # Previous transaction not found, skip this input
                    continue

                # Get the value of the previous output
                prev_output = prev_tx.get("vout", [])[vout]
                if prev_output:
                    total_input_value += prev_output.get("value", 0)

            # Calculate the total output value
            for output in tx.get("vout", []):
                total_output_value += output.get("value", 0)

            # Check if the total input value is greater than or equal to the total output value
            return total_input_value >= total_output_value

    async def validate_script(self, prev_tx, vout, script_pubkey):
        """
        Validate the input script (scriptSig or witness) against the previous output's script public key
        :param prev_tx: The previous transaction
        :param vout: The index of the previous output
        :param script_pubkey: The script public key of the previous output
        :return: True if the input script is valid, False otherwise
        """
        prev_input = prev_tx.get("vin", [])[0]  # Assuming there's only one input
        if not prev_input:
            return False

        scriptsig = prev_input.get("scriptsig")
        witness = prev_input.get("witness", [])

        print(f"scriptsig : {scriptsig}")
        print(f"witness : {witness}")
        # Validate the input script against the previous output's script public key
        # ...

        return False

    async def get_prev_tx_output(self, txid, vout) -> (list, None):
        """
        Retrieves the previous transaction output.
        :param txid: Transaction ID
        :param vout: Output index
        :return: A tuple containing the previous transaction and the specified output,
        or (None, None) if they don't exist
        """
        # Step 1: Retrieve the previous transaction
        prev_tx = await self.retrieve_transaction(txid)
        if prev_tx is None:
            print(f"Previous transaction with txid {txid} not found")
            return None, None

        prev_output = prev_tx.get("vout")
        # Step 2: Check if the specified output index exists
        if vout >= len(prev_output):
            return None, None

        # Step 3: Verify that the output is unspent
        if await self.is_spent(prev_tx, vout):
            return None, None

        # Step 4: Retrieve the script pub key from the referred output
        script_pubkey = prev_tx.get("vout")[0].get("scriptpubkey")

        # Step 5: Validate the scriptSig or Witness
        if not await self.validate_script(prev_tx, vout, script_pubkey):
            return None, None

        # Step 6: Ensure the sum of input values is greater than or equal to the sum of output values
        if not await self.validate_transaction_amount(prev_tx):
            return None, None

        return prev_tx, prev_tx.get("vout")[vout]

    async def validate_locktime_and_sequence(self, tx):
        """
        Validates the locktime and sequence fields of a transaction.
        :param tx: The transaction to validate
        :return: True if the locktime and sequence are valid, False otherwise
        """
        locktime = tx.get("locktime")
        sequence = tx.get("vin", [])[0].get("sequence", 0xFFFFFFFF)

        # Check if the transaction is a relative time-locked transaction
        if sequence < 0xFFFFFFFF:
            # Add logic to validate relative time-locked transactions
            pass

        # Check if the transaction has a non-zero locktime
        if locktime != 0:
            # Check if the locktime is a block height
            if locktime < 500000000:
                # Add logic to validate locktime as a block height
                pass
            else:
                # Validate locktime as a Unix timestamp
                current_time = int(time.time())
                if current_time < locktime:
                    return False

        return True

    async def is_spent(self, tx, vout):
        """
        Check if a specific output of a transaction has already been spent
        :param tx: The transaction to check
        :param vout: The output index to check
        :return: True if the output is spent, False otherwise
        """
        # Get the transaction ID
        txid = tx.get("txid")

        # Iterate over all transactions
        for other_tx in self.transaction_by_id.values():
            # Skip the transaction we're checking
            if other_tx.get("txid") == txid:
                continue

            # Check if any input of the other transaction spends the output we're checking
            for other_input in other_tx.get("vin", []):
                if other_input.get("txid") == txid and other_input.get("vout") == vout:
                    # Output is spent by this input
                    return True

        # Output is not spent
        return False

    async def is_double_spend(self, tx):
        """
        Check if the transaction is double spent
        :param tx: The transaction to check
        :return: True if the transaction is double spent, False otherwise
        """
        for tx_input in tx.get("vin", []):
            txid = tx_input.get("txid")
            vout = tx_input.get("vout")

            # Retrieve the previous transaction
            prev_tx = await self.retrieve_transaction(txid)
            if prev_tx is None:
                # Previous transaction not found, assume not double spent
                continue

            # Check if the referred output is already spent
            if await self.is_spent(prev_tx, vout):
                # Output is already spent, this is a double spend
                return True

        # No double spend detected
        return False

    async def validate_transaction(self, tx) -> (bool, str):
        """
        :param tx:
        :return: validated transaction
        """
        if not self.validate_transaction_version(tx):
            return False, f"Transaction has invalid version \n"

        total_input_value = 0

        for tx_input in tx.get("vin"):
            prev_tx, prev_outputs = await self.get_prev_tx_output(tx_input["txid"], tx_input["vout"])
            if not prev_outputs:
                return False, "Previous output not found"

            for prev_output in prev_outputs:
                total_input_value += prev_output["value"]

                vout = tx_input["vout"]

                if not self.verify_input_script(prev_tx, vout, prev_output["scriptpubkey"]):
                    return False, "Failed to verify input script"
                total_input_value += prev_output.get("value")

            # Validate outputs
            total_output_value = sum(output.get("value") for output in tx.get("vout"))
            if total_output_value > total_input_value:
                return False

            for output in tx.get("vout"):
                if not self.is_valid_output_script(output.get("scriptpubkey")):
                    return False

            if not self.validate_locktime_and_sequence(tx):
                return False

            if self.is_double_spend(tx):
                return False
            print("Everything is valid")
            return True
        # print("Transaction has valid version") tested

    async def validate_transactions(self, transactions):
        """
        Validates and gathers all valid transactions that would later be mined.
        :param transactions:
        :return:
        """
        tasks = [self.validate_transaction(transaction) for transaction in transactions]
        return await asyncio.gather(*tasks)