import asyncio



class ValidateTransaction:

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