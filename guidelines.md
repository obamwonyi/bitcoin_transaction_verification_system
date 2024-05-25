# Guidelines on the project solutions 

## Validation a transaction, algorithm thinking process
1. Check syntactic correctness
2. Make sure neither in or out lists are empty
3. Size in bytes < MAX_BLOCK_SIZE
4. Each output value, as well as the total, must be in legal money range
5. Make sure none of the inputs have hash=0, n=-1 (coinbase transactions)
6. Check that nLockTime <= INT_MAX[1], size in bytes >= 100[2], and sig opcount <= 2[3]
7. Reject "nonstandard" transactions: scriptSig doing anything other than pushing numbers on the stack, or scriptPubkey not matching the two usual forms[4]
8. Reject if we already have matching tx in the pool, or in a block in the main branch
9. For each input, if the referenced output exists in any other tx in the pool, reject this transaction.[5]
10. For each input, look in the main branch and the transaction pool to find the referenced output transaction. If the output transaction is missing for any input, this will be an orphan transaction. Add to the orphan transactions, if a matching transaction is not in there already.
11. For each input, if the referenced output transaction is coinbase (i.e. only 1 input, with hash=0, n=-1), it must have at least COINBASE_MATURITY (100) confirmations; else reject this transaction
12. For each input, if the referenced output does not exist (e.g. never existed or has already been spent), reject this transaction[6]
13. Using the referenced output transactions to get input values, check that each input value, as well as the sum, are in legal money range
14. Reject if the sum of input values < sum of output values
15. Reject if transaction fee (defined as sum of input values minus sum of output values) would be too low to get into an empty block
16. Verify the script PubKey accepts for each input; reject if any are bad
17. Add to transaction pool[7]
18. "Add to wallet if mine"
19. Relay transaction to peers
20. For each orphan transaction that uses this one as one of its inputs, run all these steps (including this one) recursively on that orphan

## Mining
1. Check syntactic correctness
2. Reject if duplicate of block we have in any of the three categories
3. Transaction list must be non-empty
4. Block hash must satisfy claimed nBits proof of work
5. Block timestamp must not be more than two hours in the future
6. First transaction must be coinbase (i.e. only 1 input, with hash=0, n=-1), the rest must not be
7. For each transaction, apply "tx" checks 2-4
8. For the coinbase (first) transaction, scriptSig length must be 2-100
9. Reject if sum of transaction sig opcounts > MAX_BLOCK_SIGOPS
10. Verify Merkle hash
11. Check if prev block (matching prev hash) is in main branch or side branches. If not, add this to orphan blocks, then query peer we got this from for 1st missing orphan block in prev chain; done with block
12. Check that nBits value matches the difficulty rules
13. Reject if timestamp is the median time of the last 11 blocks or before
14. For certain old blocks (i.e. on initial block download) check that hash matches known values
15. Add block into the tree. There are three cases: 1. block further extends the main branch; 2. block extends a side branch but does not add enough difficulty to make it become the new main branch; 3. block extends a side branch and makes it the new main branch.
16. For case 1, adding to main branch:
    1. For all but the coinbase transaction, apply the following:
       1. For each input, look in the main branch to find the referenced output transaction. Reject if the output transaction is missing for any input.
       2. For each input, if we are using the nth output of the earlier transaction, but it has fewer than n+1 outputs, reject.
       3. For each input, if the referenced output transaction is coinbase (i.e. only 1 input, with hash=0, n=-1), it must have at least COINBASE_MATURITY (100) confirmations; else reject.
       4. Verify crypto signatures for each input; reject if any are bad
       5. For each input, if the referenced output has already been spent by a transaction in the main branch, reject
       6. Using the referenced output transactions to get input values, check that each input value, as well as the sum, are in legal money range
       7. Reject if the sum of input values < sum of output values
    2. Reject if coinbase value > sum of block creation fee and transaction fees
    3. (If we have not rejected):
    4. For each transaction, "Add to wallet if mine"
    5. For each transaction in the block, delete any matching transaction from the transaction pool
    6. Relay block to our peers
    7. If we rejected, the block is not counted as part of the main branch
17. For case 2, adding to a side branch, we don't do anything.
18. For case 3, a side branch becoming the main branch:
    1. Find the fork block on the main branch which this side branch forks off of
    2. Redefine the main branch to only go up to this fork block
    3. For each block on the side branch, from the child of the fork block to the leaf, add to the main branch:
       1. Do "branch" checks 3-11
       2. For all but the coinbase transaction, apply the following:
          1. For each input, look in the main branch to find the referenced output transaction. Reject if the output transaction is missing for any input.
          2. For each input, if we are using the nth output of the earlier transaction, but it has fewer than n+1 outputs, reject.
          3. For each input, if the referenced output transaction is coinbase (i.e. only 1 input, with hash=0, n=-1), it must have at least COINBASE_MATURITY (100) confirmations; else reject.
          4. Verify crypto signatures for each input; reject if any are bad
          5. For each input, if the referenced output has already been spent by a transaction in the main branch, reject
          6. Using the referenced output transactions to get input values, check that each input value, as well as the sum, are in legal money range
          7. Reject if the sum of input values < sum of output values
       3. Reject if coinbase value > sum of block creation fee and transaction fees
       4. (If we have not rejected):
       5. For each transaction, "Add to wallet if mine"
    4. If we reject at any point, leave the main branch as what it was originally, done with block
    5. For each block in the old main branch, from the leaf down to the child of the fork block:
       1. For each non-coinbase transaction in the block:
          1. Apply "tx" checks 2-9, except in step 8, only look in the transaction pool for duplicates, not the main branch
          2. Add to transaction pool if accepted, else go on to next transaction
    6. For each block in the new main branch, from the child of the fork node to the leaf:
       1. For each transaction in the block, delete any matching transaction from the transaction pool
    7. Relay block to our peers
19. For each orphan block for which this block is its prev, run all these steps (including this one) recursively on that orphan

## Creating Merkel Root
* Hash 11 TXIDs together.

## Proper way to comment python codes
### Classes
```python
class MyClass:
    """
    Brief summary of the class.

    Attributes:
        attribute1 (type): Description of attribute1.
        attribute2 (type): Description of attribute2.

    Methods:
        method1(arg1, arg2): Description of method1.
        method2(arg1): Description of method2.
    """
    # Class implementation goes here
```

### Methods
```python
class MyClass:
    def my_method(self, arg1, arg2=None):
        """
        Brief summary of my_method.

        Args:
            arg1 (type): Description of arg1.
            arg2 (type, optional): Description of arg2. Defaults to None.

        Returns:
            type: Description of the return value.

        Raises:
            Exception1: Description of Exception1.
            Exception2: Description of Exception2.
        """
        # Method implementation goes here
```

## Copied Todo List:
        # Todo: Not necessary step 1 : check if transaction is unspent

        # Todo: step 2 : Validate the input's scriptSig (or witness data for SegWit inputs) against the referenced output's scriptPubKey.

        # Todo: step 3 : P2PKH
        if not await self.validate_p2pkh_script(tx):
            print("Transaction is invalid")
            return False, "The p2pkh script validation failed"

        # Todo: step 4 :  Ensure that the sum of output values does not exceed the sum of input values (minus any transaction fees).

        # Todo: step 5 : Check that no output value is negative or too large (e.g., above the maximum allowed value).

        # Todo: step 6 : Ensure that each output script is a valid script format (e.g., P2PKH, P2WPKH, P2SH, etc.) and follows the correct script structure.

        # Todo: step 7 : Calculate the transaction fee by subtracting the sum of output values from the sum of input values.

        # Todo: step 8 : Ensure that the transaction fee meets the minimum required fee rate (fees per byte) for the network.

        # Todo: step 9 : Ensure that there are no duplicate inputs (i.e., no double-spending) within the transaction.

        # Todo: step 10 : Ensure that there are no duplicate outputs (which would be considered non-standard).