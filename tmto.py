from random import getrandbits 
from random import seed
from datetime import datetime

from sbox_feistal import sbox_feistel_block


m = 2**4 # m = N^(1/3)
t = 2**4 # t = N^(1/3)


def compute_matrix(plaintext):
    matrix = list()
    for i in range(m):
        matrix.append([0 for _ in range(t)])
        for j in range(t):
            if j == 0:
                matrix[i][j] = bytearray(bin(getrandbits(12)).strip('0b').zfill(12), encoding='utf-8')
            else:
                rand_bits = bytearray(bin(getrandbits(4)).strip('0b').zfill(4), encoding='utf-8')
                matrix[i][j] = rand_bits + sbox_feistel_block(plaintext, int(matrix[i][j-1], 2))
    return matrix


def get_key(plaintext:bytearray, ciphertext: bytearray):
    precomputed_matrix = compute_matrix(plaintext)
    for i in range(m):
        for j in range(t):
            if ciphertext == precomputed_matrix[i][j][4:12] and j != 0:
                return precomputed_matrix[i][j-1]
    return -1


if __name__=="__main__":
    time = datetime.now().timestamp()
    seed(int(time))
    plaintext = b"i"
    plaintext = bin(int(plaintext.hex(), 16)).strip('0b')
    plaintext = plaintext.zfill(len(plaintext) + 8-len(plaintext)%9) # Now the plaintext is a string of 0's and 1's only
    key = getrandbits(12)
    print(f'KEY: {bin(key)}')
    ciphertext = sbox_feistel_block(plaintext, key)
    print(f"Original ciphertext {ciphertext}")
    key_found = get_key(plaintext, ciphertext)
    if key_found ==  -1:
        print("Key not found")
        exit()
    print(f"KEY FOUND {key_found}")
    key_found = int(key_found, 2)
    print(f"Final ciphertext {sbox_feistel_block(plaintext, key_found)}")
