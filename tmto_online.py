
from tmto_offline import m, t
import pickle
from random import getrandbits
from random import seed
from datetime import datetime
from sbox_feistal import sbox_feistel_system_3, sbox_feistel_block
with open('precomputed_matrix.pkl', 'rb') as f:
    precomputed_matrix = pickle.load(f)

m = 2**4 # m = N^(1/3)
t = 2**4 # t = N^(1/3)

def get_key(plaintext:bytearray, ciphertext: bytearray):
    for i in range(m):
        for j in range(t):
            if ciphertext == precomputed_matrix[i][j][4:12] and j != 0:
                print(f"i: {i}, j:{j}, matrix element: {precomputed_matrix[i][j]}")
                return precomputed_matrix[i][j-1]
    return -1

if __name__=="__main__":
    time = datetime.now().timestamp()
    seed(int(time))
    plaintext = b"i"
    plaintext = bin(int(plaintext.hex(), 16)).strip('0b')
    plaintext = plaintext.zfill(len(plaintext) + 8-len(plaintext)%9) # Now the plaintext is a string of 0's and 1's only
    key = getrandbits(12)
    print(f'KEY: {key}')
    ciphertext = sbox_feistel_block(plaintext, key)
    # plaintext = bin(int(plaintext.hex(), 16)).strip('0b')
    # plaintext = plaintext.zfill(len(plaintext) + 8-len(plaintext)%9) # Now the plaintext is a string of 0's and 1's only
    print(f"Original ciphertext {ciphertext}")
    key_found = get_key(plaintext, ciphertext)
    print(f'Key Found {key_found}')
    if key_found ==  -1:
        exit()
    key_found = int(key_found, 2)
    print(f"Final ciphertext {sbox_feistel_block(plaintext, key_found)}")


            
    