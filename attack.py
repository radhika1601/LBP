from tmto import get_key, compute_tmto_lists
from sbox_feistal import SboxFeistel
import binascii
import pickle

# TODO: Store the final matrices in sorted way for binary search.

if __name__ == "__main__":
    print("This program is to do a chosen plaintext attack on the feistel structure in sbox_feistel.")
    chosen_plaintext = bytes(
        input("Please enter your chosen plaintext\n").rstrip('\n'), encoding='utf-8')
    chosen_plaintext = int(chosen_plaintext.hex(), 16)
    # Precomutation phase begins here.
    plaintext_precomputation = chosen_plaintext
    i = 0
    while plaintext_precomputation != 0:
        plaintext_block = plaintext_precomputation % (2**8)
        block_tmto_list = compute_tmto_lists(plaintext_block)
        with open(f"block_{i}.pkl", 'wb') as f:
            pickle.dump(block_tmto_list, f)
        i += 1
        plaintext_precomputation = ( plaintext_precomputation >> 8)

    ciphertext_part = bytes(input(
        "Please enter the corresponding ciphertext as hex\n").rstrip('\n'), encoding='utf-8')
    print(f'{ciphertext_part}')
    ciphertext_part = int(ciphertext_part, 16)
    key = get_key(chosen_plaintext, ciphertext_part)
    if key is False:
        print("OOPS! Key not found")
        exit()
    sbox_feistel_system = SboxFeistel(key=key)
    assert chosen_plaintext == int(
        sbox_feistel_system.decrypt(ciphertext_part), 2)

    print(f"""
-------------------------------------------------
Cryptanalysis Complete. The final key is {key}
-------------------------------------------------
        """)

    while True:

        option = int(input("""
Please choose an option.
1. Decrypt a message with computed key
2. Quit
        """).strip('\n'), 10)

        if option == 1:

            ciphertext = bytes(input(
                "Please enter the ciphertext as hex\n").rstrip('\n'), encoding='utf-8')
            ciphertext = int(ciphertext, 16)
            p_expect = (sbox_feistel_system.decrypt(ciphertext))
            print(binascii.unhexlify("%x" % (int(p_expect, 2))))

        elif option == 2:
            exit()
        else:
            print("Invalid option")
            continue
