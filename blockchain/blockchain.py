from flask import Flask

class Blockchain:
    
    def __init__(self):
        self.transactions = []
        self.chain = []

#Instantiate blockchain
blockchain = Blockchain()

#Instantiate a node
app = Flask(__name__)

@app.route('/')
def index():
    return './index.html'


if __name__ == '__main__':
    app.run(debug=True)