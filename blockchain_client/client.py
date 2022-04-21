from flask import Flask, render_template




class Transactions:

    def __init__(self, sender_address, sender_private_key, recipient_address, value):
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.recipient_address = recipient_address
        self.value = value


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

@app.route('/wallet/new')
def new_wallet():
    return render_template('new_wallet.html')

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default = 8081, type = int, help ="Port to listen")
    args = parser.parse_args()
    port = args.port
    
    #Run flask app
    app.run(port=port, debug=True)