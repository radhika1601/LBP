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


def sbox_feistel_block(plaintext: bytearray, key: bytearray):

    left_array = plaintext[4:8]
    right_array = plaintext[0:4]
    left = int(left_array, 2)
    right = int(right_array, 2)
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
    left_array = bin(left).strip('0b')
    right_array = bin(right).strip('0b')
    left_array = left_array.zfill(len(left_array) + 4-len(left_array)%5)
    right_array = right_array.zfill(len(right_array) + 4-len(right_array)%5)
    ciphertext_block = left_array + right_array
    return bytearray(ciphertext_block, encoding='utf-8')


def sbox_feistel_system_3(plaintext, key):
    
    ciphertext = bytearray()
    for i in range(int(len(plaintext)/8)):
        plaintext_block = plaintext[8*i:8*i+8]
        ciphertext_block = sbox_feistel_block(plaintext_block, key)
        ciphertext += ciphertext_block
    print(repr(ciphertext))
    return ciphertext

def main():

    plaintext = bytes(input("Please enter your plaintext").strip('\n'), encoding='utf-8')
    plaintext = bin(int(plaintext.hex(), 16)).strip('0b')
    plaintext = plaintext.zfill(len(plaintext) + 8-len(plaintext)%9) # Now the plaintext is a string of 0's and 1's only
    key = getrandbits(12)
    print(f'KEY: {key}')
    sbox_feistel_system_3(plaintext, key)

if __name__ == '__main__':
    main()
