import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random


startinglimit = 420000
proof = startinglimit
checkedrange = range(-1, 1)
proofexhaustcounter = 0

def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    start = timer()

    print("Searching for next proof")

    global startinglimit
    global proof
    global checkedrange
    global proofexhaustcounter
    #  TODO: Your code here
    last_proof = str(last_proof)
    encoded_last = last_proof.encode()
    last_hash = hashlib.sha256(encoded_last).hexdigest()
    while valid_proof(last_hash, proof) is False:
        if startinglimit == proof:
            proof = proof * -1
        elif proof < 0:
            proof = (proof * -1) - 1
        elif proof > 0:
            proof = (proof * -1) + 1
        # Miner has exhausted a range of numbers
        elif proof in checkedrange:
            print(F"Current proof is {proof}.")
            proofexhaustcounter += 1
            checkedrange = range((startinglimit * -1), startinglimit)
            startinglimit = 420000 * (100 * (10 ** proofexhaustcounter))
            proof = startinglimit
            print(F"Exhaustion reached, increasing sample size. New starting limit is {startinglimit}.")

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """

    # TODO: Your code here!
    encoded_proof = str(proof).encode()
    hashed_proof = hashlib.sha256(encoded_proof).hexdigest()

    return last_hash[-6:] == hashed_proof[:6]


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
