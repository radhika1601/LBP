# sbox_feistel_block = E
# C, P {0, 1}^8
# K {0, 1}^12
# Let us assume chosen plaintext attack. Chosen plaintext: A
from random import getrandbits 
import pickle

from sbox_feistal import sbox_feistel_block

m = 2**4 # m = N^(1/3)
t = 2**4 # t = N^(1/3)
def compute_matrix(plaintext):
    """
    """
    matrix = list()
    for i in range(m):
        matrix.append([0 for _ in range(t)])
        for j in range(t):
            if j == 0:
                matrix[i][j] = bytearray(bin(getrandbits(12)).strip('0b').zfill(12), encoding='utf-8')
            else:
                # plaintext = matrix[i][0] [4:12]
                rand_bits = bytearray(bin(getrandbits(4)).strip('0b').zfill(4), encoding='utf-8')
                matrix[i][j] = rand_bits + sbox_feistel_block(plaintext, int(matrix[i][j-1], 2))
    return matrix

# def compute_tmto_lists():
#     # hj distinct permutation functions


if __name__=="__main__":
    plaintext = bytearray(bin(0x69).strip('0b').zfill(8), encoding='utf-8')
    offline_matrix = compute_matrix(plaintext)

    with open('precomputed_matrix.pkl', 'wb') as f:
        pickle.dump(offline_matrix, f)
