from random import getrandbits 
from random import seed, sample
from datetime import datetime
import pickle
from sbox_feistal import sbox_feistel_block

import os

m = 2**4 # m = N^(1/3)
t = 2**4 # t = N^(1/3)

def permute(j:int, x:int):
    # hj(x)
    # bin_j = bytearray(bin(j).strip('0b').zfill(4), encoding='utf-8')
    # y = bin_j + bin_j
    y = (j << 4) + j
    return  x^y

def compute_tmto_lists(plaintext):
    lists = []
    sp = sample(range(0, 2**8), m)
    # for i in range(m):
    #     el = bytearray(bin(sp[i]).strip('0b').zfill(8), encoding='utf-8')
    #     assert el not in sp, f'Fail'
    #     sp[i] = bytearray(bin(sp[i]).strip('0b').zfill(8), encoding='utf-8')
    # # print(sp)
    # for i in range
    for l_num in range(t):
        num_to_append = (l_num << 8)
        matrix = list()
        for i in range(m):
            matrix.append([0 for _ in range(t)])
            for j in range(t):
                if j == 0:
                    matrix[i][j] = num_to_append + permute(l_num, sp[i])
                else:
                    matrix[i][j] = num_to_append + sbox_feistel_block(plaintext, matrix[i][j-1])
        l = {}
        for i in range(m):
            assert matrix[i][0] not in l , f'{i}, {l_num}'
            l[matrix[i][0]] = matrix[i][t-1]
        # print(len(l))
        lists.append(matrix)
    return lists

def get_key(plaintext:bytearray, ciphertext: bytearray):
    lists = compute_tmto_lists(plaintext)
    for precomputed_matrix in lists:
        for i in range(m):
            for j in range(t):
                if ciphertext == precomputed_matrix[i][j] % (2**8)   and j != 0:
                    # print(f"i: {i}, j:{j}, matrix element: {precomputed_matrix[i][j]}")
                    return precomputed_matrix[i][j-1]
    
    # assert(len(lists) == 16)
    # for i in range(t):
    #     print(i)
    #     assert(len(lists[i]) == 16)

    # for i in range(t):
    #     num_to_append = (i << 8)
    #     for j in range(t):
    #         c = num_to_append + ciphertext
    #         c_i = c
    #         for x in range(i):
    #             c_i = num_to_append + sbox_feistel_block(plaintext, c_i)
    #         for l in range(m):
    #             for k, value in lists[j].items():
    #                 if c_i == value:
    #                     x_l0 = k
    #                     key = x_l0
    #                     y = key
    #                     for i in range(t-1):
    #                         y = num_to_append + sbox_feistel_block(plaintext, y)
    #                     assert( value == y)
    #                     for x in range(t- i - 2):
    #                         key = num_to_append + sbox_feistel_block(plaintext, key)
    #                     y = key
    #                     for x in range(i+1):
    #                         y = num_to_append + sbox_feistel_block(plaintext, y)
    #                     assert( value == y )
    #                     ciphertext_expected = sbox_feistel_block(plaintext, key)
    #                     c_expected = num_to_append + ciphertext_expected
    #                     for x in range(i):
    #                         c_expected = num_to_append + sbox_feistel_block(plaintext, c_expected)
    #                     assert( value == c_expected )
    #                     print(ciphertext, ciphertext_expected)
    #                     assert(ciphertext == ciphertext_expected)
    #                     return key
    return False                

if __name__=="__main__":
    time = datetime.now().timestamp()
    seed(int(time))
    plaintext = b"i"
    # plaintext = bin(int(plaintext.hex(), 16)).strip('0b')
    # plaintext = plaintext.zfill(len(plaintext) + 8-len(plaintext)%9) # Now the plaintext is a string of 0's and 1's only
    plaintext = int(plaintext.hex(), 16)
    key = getrandbits(12)
    print(f'KEY: {bin(key)}')
    ciphertext = sbox_feistel_block(plaintext, key)
    # print(f"Original ciphertext {ciphertext}")
    key_found = get_key(plaintext, ciphertext)
    if key_found ==  False:
        print("Key not found")
        exit()
    print(f"KEY FOUND {key_found}")
    # key_found = int(key_found, 2)
    final = sbox_feistel_block(plaintext, key_found)
    # print(f"Final ciphertext {sbox_feistel_block(plaintext, key_found)}")
    assert( ciphertext == final )
    # with open('correct_matrix.pkl', 'wb') as f:
    # print(int(time))
    # key_found = b'001100110001'
    # c_i = b'001110010111'
    # assert( bytearray(c_i) == sbox_feistel_block(plaintext, int(key_found, 2)) )