from flask import Flask, render_template
from time import time




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


#Instantiate blockchain
blockchain = Blockchain()

#Instantiate a node
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./index.html')


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default = 5001, type = int, help ="Port to listen")
    args = parser.parse_args()
    port = args.port
    
    #Run flask app
    app.run(port=port, debug=True)