from Crypto.Util.strxor import strxor
from Crypto.Util.Padding import pad
from random import getrandbits
import binascii

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


def sbox_dec(state: int):
    switcher = {
        0xC: 0x0,
        0x5: 0x1,
        0x6: 0x2,
        0xB: 0x3,
        0x9: 0x4,
        0x0: 0x5,
        0xA: 0x6,
        0xD: 0x7,
        0x3: 0x8,
        0xE: 0x9,
        0xF: 0xA,
        0x8: 0xB,
        0x4: 0xC,
        0x7: 0xD,
        0x1: 0xE,
        0x2: 0xF,
    }
    return switcher.get(state)


class SboxFeistel():

    def __init__(self, key):
        self.key = key

    def get_round_keys(self, **kwargs):
        round_keys = list()
        if kwargs.get('key', None) is not None:
            key = kwargs.get('key')
        else:
            key = self.key
        round_keys.append(((key & 0xf0) >> 4) ^ ((key & 0xf00) >> 8))
        round_keys.append(key & 0xf ^ ((key & 0xf0) >> 4))
        round_keys.append(key & 0xf ^ ((key & 0xf00) >> 8))

        return round_keys

    def decrypt_block(self, c_block: int, **kwargs):
        round_keys = self.get_round_keys(key=kwargs.get('key', None))
        left = c_block % (2**4)
        right = (c_block >> 4) % (2**4)

        for i in range(NUM_ROUNDS):
            if i != 0:
                left = sbox_dec(left)
                right = sbox_dec(right)
            left_new = right
            right = left ^ round_keys[NUM_ROUNDS-i-1] ^ right
            left = left_new
        plaintext_block = (left << 4) + right
        return plaintext_block

    def encrypt_block(self, plaintext: int, **kwargs):

        left = plaintext % (2**4)
        right = (plaintext >> 4) % (2**4)

        round_keys = self.get_round_keys(key=kwargs.get('key', None))

        for i in range(NUM_ROUNDS):
            left_new = right
            right = left ^ round_keys[i] ^ right
            left = left_new
            if i < NUM_ROUNDS - 1:
                left = sbox(left)
                right = sbox(right)
        ciphertext_block = (left << 4) + right
        return ciphertext_block

    def encrypt(self, plaintext: int, **kwargs):
        ciphertext = bytearray()
        p = plaintext
        i = 0
        while p != 0:
            plaintext_block = p % (2**8)
            ciphertext_block = self.encrypt_block(
                plaintext_block, key=kwargs.get('key', None))
            ciphertext = bytearray(bin(ciphertext_block).lstrip(
                '0b').zfill(8), encoding='utf-8') + ciphertext
            p = p >> 8
        return ciphertext

    def decrypt(self, ciphertext: int, **kwargs):
        plaintext = bytearray()
        while ciphertext != 0:
            c_block = ciphertext % (2**8)
            plaintext_block = self.decrypt_block(
                c_block, key=kwargs.get('key', None))
            plaintext = bytearray(bin(plaintext_block).lstrip(
                '0b').zfill(8), encoding='utf-8') + plaintext
            ciphertext = ciphertext >> 8
        return plaintext


def test_block():
    p = b'a'
    p_int = int(p.hex(), 16)
    key = 2332
    sbox_feistal = SboxFeistel(key)
    c = sbox_feistal.encrypt_block(p_int)
    p_expect = sbox_feistal.decrypt_block(c)
    assert p_int == p_expect


def test_system():
    p = b'Does this even work?'
    p_int = int(p.hex(), 16)
    key = 2332
    sbox_feistal = SboxFeistel(key)
    c = sbox_feistal.encrypt(p_int)
    p_expect = sbox_feistal.decrypt(int(c, 2))
    p_expect = binascii.unhexlify("%x" % (int(p_expect, 2)))
    assert p_expect == p
    print(binascii.unhexlify("%x" % (int(c, 2))))

    c_int = int(sbox_feistal.encrypt(p_int), 2)
    while p_int != 0:
        p_block = p_int % (2**8)
        assert (c_int % (2**8)) == sbox_feistal.encrypt_block(p_block)
        p_int = p_int >> 8
        c_int = c_int >> 8


def main():

    plaintext = bytes(
        input("Please enter your plaintext\n").rstrip('\n'), encoding='utf-8')
    plaintext = int(plaintext.hex(), 16)
    key = getrandbits(12)
    print(f'KEY: {key}')
    sbox_feistel_system_3(plaintext, key)


if __name__ == '__main__':
    # main()
    test_block()
    test_system()
