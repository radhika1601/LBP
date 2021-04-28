from random import getrandbits 
from random import seed
from datetime import datetime

from sbox_feistal import sbox_feistel_block


m = 2**4 # m = N^(1/3)
t = 2**4 # t = N^(1/3)

def permute(j:int, x:bytearray):
    # hj(x)
    bin_j = bytearray(bin(j).strip('0b').zfill(4), encoding='utf-8')
    y = bin_j + bin_j
    y = int(y, 2)
    return  bytearray( bin( int(x, 2)^y ).strip('0b').zfill(8), encoding='utf-8' )

def compute_tmto_lists(plaintext):
    lists = []
    sp = []
    for i in range(m):
        sp.append(bytearray(bin(getrandbits(8)).strip('0b').zfill(8), encoding='utf-8'))
    for l_num in range(t): 
        bits_to_append = bytearray( bin(l_num).strip('0b').zfill(4), encoding='utf-8' )
        matrix = list()
        for i in range(m):
            matrix.append([0 for _ in range(t)])
            for j in range(t):
                if j == 0:
                    matrix[i][j] = bits_to_append + permute(l_num, sp[j])
                else:
                    matrix[i][j] = bits_to_append + sbox_feistel_block(plaintext, int(matrix[i][j-1], 2))
        l = {}
        for i in range(m):
            l[int(matrix[i][0], 2)] = matrix[i][t-1]
        lists.append(l)
    return lists

def get_key(plaintext:bytearray, ciphertext: bytearray):
    lists = compute_tmto_lists(plaintext)
    # for precomputed_matrix in lists:
    #     for i in range(m):
    #         for j in range(t):
    #             if ciphertext == precomputed_matrix[i][j][4:12] and j != 0:
    #                 print(f"i: {i}, j:{j}, matrix element: {precomputed_matrix[i][j]}")
    #                 return precomputed_matrix[i][j-1]
    for i in range(t):
        bits_to_append = bytearray( bin(i).strip('0b').zfill(4), encoding='utf-8' )
        # for j in range(t):
            # c = bits_to_append + ciphertext
            # c_i = c
            # for x in range(i):
            #     c_i = bits_to_append + sbox_feistel_block(plaintext, int(c_i, 2))
            # for l in range(m):
            #     for k, value in lists[j].items():
            #         if c_i == value:
            #             x_l0 = k
            #             key = bytearray( bin(x_l0).strip('0b').zfill(12), encoding='utf-8')
            #             y = key
            #             for i in range(t):
            #                 y = bits_to_append + sbox_feistel_block(plaintext, int(y, 2))
            #             assert( value == y)
            #             for x in range(t-i-1):
            #                 key = bits_to_append + sbox_feistel_block(plaintext, int(key, 2))
            #             y = key
            #             for x in range(i+1):
            #                 y = bits_to_append + sbox_feistel_block(plaintext, int(y, 2))
            #             assert( value == y )
            #             assert( c == sbox_feistel_block(plaintext, int(key, 2)) )
            #             return key
    return False                

if __name__=="__main__":
    # time = datetime.now().timestamp()
    # seed(int(time))
    plaintext = b"i"
    plaintext = bin(int(plaintext.hex(), 16)).strip('0b')
    plaintext = plaintext.zfill(len(plaintext) + 8-len(plaintext)%9) # Now the plaintext is a string of 0's and 1's only
    key = getrandbits(12)
    print(f'KEY: {bin(key)}')
    ciphertext = sbox_feistel_block(plaintext, key)
    # print(f"Original ciphertext {ciphertext}")
    key_found = get_key(plaintext, ciphertext)
    if key_found ==  False:
        print("Key not found")
        exit()
    print(f"KEY FOUND {key_found}")
    key_found = int(key_found, 2)
    final = sbox_feistel_block(plaintext, key_found)
    # print(f"Final ciphertext {sbox_feistel_block(plaintext, key_found)}")
    assert( ciphertext == final )
    # key_found = b'001100110001'
    # c_i = b'001110010111'
    # assert( bytearray(c_i) == sbox_feistel_block(plaintext, int(key_found, 2)) )