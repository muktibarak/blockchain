# Module -1 creating a blockchain

# We need two things for this 
# flask - This module has been using flask 1.1.2 [cmd to install flask: 
# pip install flask==version]

# We also need postman for communicating with blockchain. We will do that in 
# next module.

# importing required libs

import datetime
import hashlib
import json
from flask import Flask, jsonify

# part 1 building a blockchain
class Blockchain:
    #We include genesis block
    #initialize chain
    #createBlock function
    #solid blockchain 
    def __init__(self):
        #the chain should be list of blocks
        self.chain = []
        # genesis block needs to be initialized
        self.create_block(proof = 1, previous_hash = '0')
        
    #define create_block which creates genesis block
    def create_block(self, proof, previous_hash):
        #block is a variable which is a dictionary
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash
                 }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        #return last index of the chain
        return self.chain[-1] 
    
    #consensus algorithm PoW needs to be defined
    def get_proof_of_work(self, previous_proof):
        #we need a variable that gets initialized by 1 to loop later
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            #if first 4 chars of hash is '0'
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
                
        return new_proof

    #hash function to return hash value of our block
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
        
    # MAKE FINAL FUNCTION TO CHECK HASH VALIDITY
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            #get the current block
            block = chain[block_index]
            #compare previous hash is the hash of previous block
            if block['previous_hash'] != self.hash():
                return False
            #check each block's validity
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            #if this has has 4 leading '0'
            if hash_operation[:4] != '0000':
                return False
            #update loop variable of the block index and previous_block
            previous_block = block
            block_index = block_index + 1
        return True

# part 2 mining our blockchain
# creating webapp

app = Flask(__name__)

#creating Blockchain
blockchain = Blockchain()

#Mining a new block
#get Flask decorator to define URL and also define the method GET
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.get_proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'A new block has been mined!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

#getting the full blockchain
@app.route('/full_blockchain', methods = ['GET'])
def get_full_blockchain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

#checking if blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'This blockchain is valid.'}
    else:
        response = {'message': 'Oops! Not a valid blockchain!'}
    return jsonify(response), 200


#Running the app
app.run(host = '0.0.0.0', port = 5000)