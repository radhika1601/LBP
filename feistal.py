from Crypto.Util.strxor import strxor
from Crypto.Util.Padding import pad
from random import getrandbits

KEY_LENGTH = 12
BLOCK_SIZE = 8
NUM_ROUNDS = 3


def feistel_block(plaintext: bytearray, key: bytearray):

    left_array = plaintext[4:8]
    right_array = plaintext[0:4]

    round_keys = list()

    round_keys.append(((key & 0xf0) >> 4) ^ ((key & 0xf00) >> 8))
    round_keys.append(key & 0xf ^ ((key & 0xf0) >> 4))
    round_keys.append(key & 0xf ^ ((key & 0xf00) >> 8))
    # print(round_keys)
    for i in range(NUM_ROUNDS):
        left_array_new = right_array
        right_array = bin(int(left_array, 2) ^ round_keys[i]).strip('0b')
        left_array = left_array_new
    # print(f'LEFT: {left_array} RIGHT: {right_array}')
    left_array = left_array.zfill(len(left_array) + 4-len(left_array) % 5)
    right_array = right_array.zfill(len(right_array) + 4-len(right_array) % 5)
    ciphertext_block = left_array + right_array
    return bytearray(ciphertext_block, encoding='utf-8')


def feistel_system_3(plaintext, key):

    ciphertext = ''
    for i in range(int(len(plaintext)/8)):
        plaintext_block = plaintext[8*i:8*i+8]
        ciphertext_block = feistel_block(plaintext_block, key)
        ciphertext += chr(int(ciphertext_block, 2))
    print(repr(ciphertext))


def main():

    plaintext = bytes(
        input("Please enter your plaintext").strip('\n'), encoding='utf-8')
    plaintext = bin(int(plaintext.hex(), 16)).strip('0b')
    # Now the plaintext is a string of 0's and 1's only
    plaintext = plaintext.zfill(len(plaintext) + 8-len(plaintext) % 9)
    key = getrandbits(12)
    print(f'KEY: {key}')
    feistel_system_3(plaintext, key)


if __name__ == '__main__':
    main()
