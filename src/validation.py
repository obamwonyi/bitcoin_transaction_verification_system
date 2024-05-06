import asyncio


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
        :param scriptpubkey:
        :return:
        """

    async def validate_transaction_amount(self, tx) -> bool:
        """
        Validates the transaction amount
        :param tx:
        :return: bool
        """
        # Implement logic to validate the transaction amount
        pass

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

        return prev_tx, prev_output

        # Step 3: Verify that the output is unspent
        # if not await self.is_unspent(prev_tx, vout):
        #     return None, None

        # # Step 4: Retrieve the script pub key from the referred output
        # script_pubkey = prev_tx.get("vout")[0].get("scriptpubkey")
        #
        # # Step 5: Validate the scriptSig or Witness
        # if not await self.validate_script(prev_tx, vout, script_pubkey):
        #     return None, None

        # Step 6: Ensure the sum of input values is greater than or equal to the sum of output values
        if not await self.validate_transaction_amount(prev_tx):
            return None, None

        return prev_tx, prev_tx.get("vout")[vout]

    async def validate_locktime_and_sequence(self, tx):
        """
        Validates Transactions locktime
        :param tx:
        :return:
        """
        pass

    async def is_double_spend(self, tx):
        """
        Check if the transaction is double spent
        :param tx:
        :return:
        """
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