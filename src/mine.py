

class Mine:
    """
    This class holds method for mining a block
    """
    def mine_block(valid_transactions) -> str:
        """
        Mine all blocks from all the valid transactions

        :param valid_transactions: all the validated transactions
        :return: str
        """
        block_data = "Block header\nCoinbase transaction\n"
        for transaction in valid_transactions:
            block_data += f"{transaction.txid}\n"
        return block_data
