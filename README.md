## Bitcoin Transaction Verification System

### About
This program is mainly focused on the various scripts that verifies is a particular transaction
from he mempool folder is valid, if valid it is added to a batch of transactions that are to be mined as a block
and added to the blockchain. In summary, it is a basic implementation of the Bitcoin mining process.


### Key Functionalities
#### 1. Transaction Validation with the various scripts
| Scripts | Implementation Status |
|---------|-----------------------|
| P2PK    | 0                     |
| P2PKH   | 1                     |
| P2MS    | 0                     |
| P2SH    | 0                     |
| P2WPKH  | 0                     |
| P2WSH   | 0                     |
*0 = Has not been implemented , 1 = has been implemented*

#### 2. Block Mining Proocess
This takes a collection of the valid transactions and try to create a block from them to 
add to the blockchain, the below approach is taken for this process.

* **Transaction Hashing**: <br>
Each individual transaction is hashed using a cryptographic hash function, typically SHA-256 (Secure Hash Algorithm 256-bit).
The transaction data, including the inputs, outputs, and other metadata, is serialized into a byte stream.
This byte stream is then passed through the SHA-256 hash function, producing a fixed-size 256-bit (32-byte) hash value, often referred to as the transaction ID (txid).


* **Merkle Tree Construction**: <br>
All the transaction IDs (hashes) in a block are combined into a Merkle Tree data structure.
A Merkle Tree is a binary tree where every non-leaf node is the hash of its two child nodes.
The leaf nodes of the Merkle Tree are the transaction IDs.
The hashes of the transactions are combined in pairs, and the hash of each pair is calculated using a hash function (typically SHA-256 again).
This process continues up the tree, creating parent nodes by hashing pairs of child nodes, until a single root hash is obtained, known as the Merkle Root.


* **Block Header Construction**: <br>
The Merkle Root is included in the block header, along with other metadata such as the previous block hash, timestamp, nonce, and difficulty target.
The block header is serialized into a byte stream.


* **Block Hashing**:
The serialized block header is passed through a double SHA-256 hash function (SHA-256 applied twice).
The resulting 256-bit (32-byte) hash value is the block hash or block ID.


### Contributors 
*responsible for blockchain validation automation with Github actions* <br>
https://github.com/theanmolsharma <br>
https://github.com/adi-shankara  <br>

### Reference
* https://learnmeabitcoin.com/
* https://developer.bitcoin.org/
* Grokking Bitcoin ( https://www.amazon.com/Grokking-Bitcoin-Kalle-Rosenbaum/dp/1617294640 )