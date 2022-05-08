from typing import OrderedDict
from flask import Flask, request, jsonify, render_template
from time import time
from flask_cors import CORS #Cross-origin resource sharing policy (allow requests between port 8001 and 5001)
from collections import OrderedDict
import binascii
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from uuid import uuid4
import json
import hashlib

MINING_SENDER ="From the blockchain"
MINING_REWARD = 1

class Blockchain:
    
    def __init__(self):
        self.transactions = []
        self.chain = []
        #Create id for each node
        #Remove all dashes from generate uuid
        self.node_id = str(uuid4()).replace('-','')
        #Create genesis block
        self.create_block(0,'0'*64)
    

    #Add a block to the blockchain
    def create_block(self, nonce, previous_hash):
        block = {   
            'block_number': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'nonce': nonce,
            'previous_hash': previous_hash
        }
        #Reset current list of transactions
        self.transactions = []
        #Add the block to the blockchain
        self.chain.append(block)
        return block

    #Verify transaction signature
    def verify_transaction_signature(self, sender_public_key, signature, transaction) :
        #Get actual public key using unhexlify
        public_key = RSA.importKey(binascii.unhexlify(sender_public_key))
        verifier = PKCS1_v1_5.new(public_key)
        #Generate hash using SHA
        h = SHA.new(str(transaction).encode('utf8'))
        #Verify the signature using the hash and public key
        try:
            verifier.verify(h, binascii.unhexlify(signature))
            return True
        except ValueError:
            return False

    
    #Signature validation and Rewards for miner
    def submit_transaction(self, sender_public_key, recipient_public_key, signature, amount):
        
        transaction = OrderedDict({
            'sender_public_key' : sender_public_key,
            'recipient_public_key' : recipient_public_key,
            'amount': amount
        })

        #Reward the miner with Netherite ingots for mining a block
        if sender_public_key == MINING_SENDER:
            self.transactions.append(transaction)
            return len(self.chain) + 1

        #Normal transaction (not a reward from blockchain)
        else:
            #Verify the transaction signature
            signature_verification = self.verify_transaction_signature(sender_public_key, signature, transaction)
            if signature_verification:
                #Append current transaction to list of transactions
                self.transactions.append(transaction)
                #No. of block to be mined
                return len(self.chain) + 1
    
    #Implement proof of work function and difficulty
    def proof_of_work(self):
        return 69676

    
    #Function to hash the block
    def hash(self, block):
        #Convert block data from dictionary to string
        #Dictionary should be ordered to prevent inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode('utf-8')
        #Hash with SHA256 algorithm
        h=hashlib.new('sha256')
        h.update(block_string)

        return h.hexdigest()

#Instantiate blockchain
blockchain = Blockchain()

#Instantiate a node
app = Flask(__name__)
CORS(app) #Cross origin resource sharing policy

@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/transactions/get', methods=['GET'])
def get_transaction():
    transactions = blockchain.transactions
    response ={'transactions' : transactions}
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def get_chain():
    response ={
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/mine', methods=['GET'])
def mine():
    #Getting nonce from POW function
    nonce = blockchain.proof_of_work()

    blockchain.submit_transaction(sender_public_key=MINING_SENDER,
                                 recipient_public_key=blockchain.node_id,
                                 signature='',
                                 amount = MINING_REWARD)
    #Get last block from blockchain
    last_block = blockchain.chain[-1]
    #Calculate hash of last block(i.e. previous block)
    previous_hash = blockchain.hash(last_block)
    block = blockchain.create_block(nonce, previous_hash)

    response = {
        'message' : 'New block created successfully',
        'block_number' : block['block_number'],
        'transactions' : block['transactions'],
        'nonce' : block['nonce'],
        'previous_hash' : block['previous_hash']
    }

    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.form

    # Check the fields for missing values
    required =['confirmation_sender_public_key', 'confirmation_recipient_public_key', 'transaction_signature', 'confirmation_amount']
    if not all(k in values for k in required):
        return 'Values are missing', 400
   
    transaction_results = blockchain. submit_transaction(values['confirmation_sender_public_key'], values['confirmation_recipient_public_key'], values['transaction_signature'], values['confirmation_amount'])
    if transaction_results == False:
        response = {
            'message' : 'Invalid Transaction'
        }
        return jsonify(response), 406
    else:
        response = {
            'message' : 'Transaction will be added to the Block' + str(transaction_results)
        }
        return jsonify(response), 201


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default = 5001, type = int, help ="Port to listen")
    args = parser.parse_args()
    port = args.port
    
    #Run flask app
    app.run(port=port, debug=True)