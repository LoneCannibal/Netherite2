from cgitb import reset
from flask import Flask, jsonify, request, render_template
import Crypto
import Crypto.Random
from Crypto.PublicKey import RSA
import binascii
from collections import OrderedDict
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA


class Transaction:

    def __init__(self, sender_public_key, sender_private_key, recipient_public_key, amount):
        self.sender_public_key = sender_public_key
        self.sender_private_key = sender_private_key
        self.recipient_public_key = recipient_public_key
        self.amount = amount


    #Function to convert transaction details to dictionary format
    def to_dict(self):
        return OrderedDict({
            'sender_public_key' : self.sender_public_key,
            'sender_private_key' : self.sender_private_key,
            'recipient_public_key' : self.recipient_public_key,
            'amount' : self.amount
        })

    #Function to sign the transaction
    def sign_transaction(self):
        private_key = RSA.importKey(binascii.unhexlify(self.sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        hash = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign (hash)).decode('ascii')




app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make/transactions')
def make_transactions():
    return render_template('make_transactions.html')

@app.route('/view/transactions')
def view_transactions():
    return render_template('view_transactions.html')


#Public and private key pair generation for wallet
@app.route('/wallet/new')
def new_wallet():
    random_gen = Crypto.Random.new().read
    private_key = RSA.generate(1024, random_gen)
    public_key = private_key.publickey()

    response={
        'private_key' : binascii.hexlify(private_key.export_key(format('DER'))).decode('ascii'),
        'public_key' :binascii.hexlify(public_key.export_key(format('DER'))).decode('ascii')
    }

    return response


#Code to generate the transactions
@app.route('/generate/transactions', methods=['POST'])
def generate_transactions():
    #Extract transaction details from form
    sender_public_key = request.form['sender_public_key']
    sender_private_key =  request.form['sender_private_key']
    recipient_public_key = request.form['recipient_public_key']
    amount = request.form['amount']

    #Make a Transaction object
    transaction = Transaction(sender_public_key, sender_private_key, recipient_public_key, amount)

    #Convert Transaction object into dictionary and sign it
    response ={'transaction' : transaction.to_dict(),
                'signature' : transaction.sign_transaction()}


    return response


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default = 8081, type = int, help ="Port to listen")
    args = parser.parse_args()
    port = args.port
    
    #Run flask app
    app.run(port=port, debug=True)