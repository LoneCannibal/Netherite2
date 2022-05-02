from typing import OrderedDict
from flask import Flask, request, jsonify, render_template
from time import time
from flask_cors import CORS #Cross-origin resource sharing policy (allow requests between port 8001 and 5001)
from collections import OrderedDict

class Blockchain:
    
    def __init__(self):
        self.transactions = []
        self.chain = []
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
        self.chain.append(block)


    def submit_transaction(self, sender_public_key, recipient_public_key, signature, amount):
        #TODO: Reward the miner with Netherite ingots
        #TODO: Validate the signature

        transaction = OrderedDict({
            'sender_public_key' : sender_public_key,
            'recipient_public_key': recipient_public_key,
            'signature': signature,
            'amount': amount
        })
        signature_verification = True
        if signature_verification:
            #Append current transaction to list of transactions
            self.transactions.append(transaction)
            #No. of block to be mined
            return len(self.chain) + 1 
        return 3

#Instantiate blockchain
blockchain = Blockchain()

#Instantiate a node
app = Flask(__name__)
CORS(app) #Cross origin resource sharing policy

@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.form

    # TODO: Check the fields
   


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