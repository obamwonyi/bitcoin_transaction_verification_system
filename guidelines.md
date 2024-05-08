# Guidelines and Restrictions

## Guidelines

1. Implement the transaction validation logic manually without using Bitcoin-specific libraries or frameworks.
2. Implement the mining algorithm yourself, including creating the block header, calculating the hash, and finding a valid nonce that meets the difficulty target.
3. Use standard cryptographic libraries (e.g., secp256k1 for elliptic curve cryptography, SHA-256 for hashing) as needed.
4. Document your work in the `SOLUTION.md` file, explaining your design approach, implementation details, results, and conclusions.
5. Publish your solution in the designated private repository, and do not share it publicly or with peers.

## Restrictions

1. Do not use any Bitcoin-specific libraries or frameworks that automate transaction validation processes.
2. Do not use existing implementations of the mining algorithm or block construction logic.
3. Do not plagiarize or copy solutions from others (solutions will be checked for plagiarism).
4. While you can use AI tools like ChatGPT to gather information and explore alternative approaches, do not rely solely on AI for complete solutions. Verify and validate any insights obtained, and maintain a balance between AI assistance and independent problem-solving.

The main objective of these guidelines and restrictions is to deepen your understanding of Bitcoin fundamentals by implementing the transaction validation and block mining processes from scratch, without relying on existing libraries or implementations. This exercise is designed to test your problem-solving skills and your ability to implement complex algorithms independently.


># Asynchronous Transaction Validation and Mining

In this assignment, you should treat the transaction validation and mining process as an asynchronous operation. Here's how you can approach it:
## 1. Fetch transactions from mempool asynchronously

- Create a function or method that reads all the JSON files in the `mempool` directory asynchronously.
- Use Python's built-in `asyncio` module or a third-party library like `aiofiles` to read the files concurrently.
- Deserialize each JSON transaction into your `Transaction` data structure.

## 2. Validate transactions asynchronously

- Create a function or method that takes a list of `Transaction` objects and validates them asynchronously.
- Use Python's `asyncio` module and its `gather` function to run the validation tasks concurrently.
- For each transaction, call your transaction validation functions or methods (implemented in `validation.py`) to check if it's valid or not.

## 3. Store valid transactions in a dictionary

- Create an empty dictionary (or any suitable data structure) to store the valid transactions.
- After the asynchronous validation is complete, iterate through the list of validated transactions and add the valid ones to the dictionary.
- Use the transaction ID (`txid`) as the key and the `Transaction` object as the value in the dictionary.

## 4. Mine the block

- In your mining logic (implemented in `mining.py`), iterate through the dictionary of valid transactions and construct the block accordingly.
- Create the coinbase transaction and include it in the block.
- Serialize the block header and coinbase transaction, and write them to the `output.txt` file as per the specified format.
- Write the transaction IDs (`txid`) of the valid transactions to the `output.txt` file, following the coinbase transaction.

## 5. Implement concurrency control

- Since multiple tasks are running concurrently, you may need to implement proper synchronization mechanisms to avoid race conditions or data corruption.
- Use Python's `asyncio` locks, semaphores, or other synchronization primitives to control access to shared resources, such as the dictionary of valid transactions.

