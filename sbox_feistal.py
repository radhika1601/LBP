from Crypto.Util.strxor import strxor
from Crypto.Util.Padding import pad
from random import getrandbits 


KEY_LENGTH = 12
BLOCK_SIZE = 8
NUM_ROUNDS = 3

def sbox(state: int):
    switcher = {
        0x0: 0xC,
        0x1: 0x5,
        0x2: 0x6,
        0x3: 0xB,
        0x4: 0x9,
        0x5: 0x0, 
        0x6: 0xA,    
        0x7: 0xD,
        0x8: 0x3,
        0x9: 0xE,
        0xA: 0xF,
        0xB: 0x8,
        0xC: 0x4,
        0xD: 0x7,
        0xE: 0x1,
        0xF: 0x2,
    }
    return switcher.get(state)


def sbox_feistel_block(plaintext: int, key: int):

    # left_array = 
    # right_array = 
    left = plaintext % (2**4)
    right = (plaintext >> 4) % (2**4)
    round_keys = list()
    
    round_keys.append(((key&0xf0)>>4) ^ ((key&0xf00)>>8))
    round_keys.append(key&0xf ^ ((key&0xf0)>>4))
    round_keys.append(key&0xf ^ ((key&0xf00)>>8))

    for i in range(NUM_ROUNDS):
        left_new = right
        right = left^round_keys[i]
        left = left_new
        if i < NUM_ROUNDS - 1:
            left = sbox(left)
            right = sbox(right)
    # left_array = bin(left).lstrip('0b')
    # right_array = bin(right).lstrip('0b')
    # left_array = left_array.zfill(len(left_array) + 4-len(left_array)%5)
    # right_array = right_array.zfill(len(right_array) + 4-len(right_array)%5)
    ciphertext_block = left << 4 + right
    return ciphertext_block


def sbox_feistel_system_3(plaintext: int, key:int):
    ciphertext = -1
    # ciphertext = bytearray()
    p = plaintext
    i = 0
    while True:
        plaintext_block = plaintext%(2**8)
        ciphertext_block = sbox_feistel_block(plaintext_block, key)
        ciphertext += (ciphertext_block << (2**(8*i)))
        i += 1
    return ciphertext
    # for i in range(int(len(plaintext)/8)):
    #     plaintext_block = plaintext[8*i:8*i+8]
    #     ciphertext_block = sbox_feistel_block(plaintext_block, key)
    #     ciphertext += ciphertext_block
    # print(repr(ciphertext))
    # return ciphertext

def main():

    plaintext = bytes(input("Please enter your plaintext").rstrip('\n'), encoding='utf-8')
    # plaintext = bin(int(plaintext.hex(), 16)).lstrip('0b')
    # plaintext = plaintext.zfill(len(plaintext) + 8-len(plaintext)%9) # Now the plaintext is a string of 0's and 1's only
    plaintext = int(plaintext.hex(), 16)
    key = getrandbits(12)
    print(f'KEY: {key}')
    sbox_feistel_system_3(plaintext, key)

if __name__ == '__main__':
    main()
