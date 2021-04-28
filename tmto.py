from random import getrandbits 
from random import seed, sample
from datetime import datetime
import pickle
from sbox_feistal import sbox_feistel_block, sbox_feistel_system_3


m = 2**4 # m = N^(1/3)
t = 2**4 # t = N^(1/3)

def permute(j:int, x:int):
    y = (j << 4) + j
    return  x^y

def compute_tmto_lists(plaintext):
    lists = []
    sp = sample(range(0, 2**8), m)
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
        lists.append(l)
    return lists

def get_key(plaintext:int, ciphertext: int):
    lists = compute_tmto_lists(plaintext)

    assert(len(lists) == 16)
    for i in range(t):
        assert(len(lists[i]) == 16)
    
    for i in range(t):
        num_to_append = (i << 8)
        c = num_to_append + ciphertext
        for column in range(1, t):
            c_t = c
            for x in range(t - 1 - column):
                c_t = num_to_append + sbox_feistel_block(plaintext, c_t)
            for k, value in lists[i].items():
                if c_t == value:
                    x_l0 = k
                    key = x_l0
                    for x in range( column - 1 ):
                        key = num_to_append + sbox_feistel_block(plaintext, key)
                    c_expected = num_to_append + sbox_feistel_block(plaintext, key)
                    if c == c_expected:
                        return key
                    else:
                        # If collision occurs but it is not the right key
                        continue
    return False

if __name__=="__main__":
    time = datetime.now().timestamp()
    seed(int(time))

    plaintext = bytes(input("Please enter your plaintext\n").rstrip('\n'), encoding='utf-8')
    plaintext = int(plaintext.hex(), 16)
    key = getrandbits(12)
    original_plaintext = plaintext
    print(f'KEY: {key}')
    while plaintext != 0:
        plaintext_block = plaintext%(2**8)
        ciphertext_block = sbox_feistel_block(plaintext_block, key)   
        key_found = get_key(plaintext_block, ciphertext_block)
        if key_found !=  False:
            ciphertext = sbox_feistel_system_3(original_plaintext, key)
            final = sbox_feistel_system_3(original_plaintext, key_found)
            if ciphertext == final:
                break
        plaintext = plaintext >> 8
        if plaintext == 0:
            print("Key not found")  
            exit()
    print(f"KEY FOUND {key_found}")
    ciphertext = sbox_feistel_system_3(original_plaintext, key)
    final = sbox_feistel_system_3(original_plaintext, key_found)
            
    assert( ciphertext == final )

