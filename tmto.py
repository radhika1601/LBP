from random import getrandbits
from random import seed, sample
from datetime import datetime
import pickle
from sbox_feistal import SboxFeistel

sbox_feistel_system = SboxFeistel(2332)
m = 2**4  # m = N^(1/3)
t = 2**4  # t = N^(1/3)


def permute(j: int, x: int):
  y = (j << 4) + j
  return x ^ y


def compute_tmto_lists(plaintext, m1=m):
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
          matrix[i][j] = num_to_append + \
            sbox_feistel_system.encrypt_block(
              plaintext, key=matrix[i][j-1])
    l = {}
    for i in range(m):
      l[matrix[i][t-1]] = matrix[i][0]
    l = {k: v for k, v in sorted(l.items(), key=lambda item: item[1])}
    lists.append(l)
  return lists


def get_key_block(plaintext: int, ciphertext: int, block_idx: int):
  with open(f"block_{block_idx}.pkl", "rb") as f:
    lists = pickle.load(f)

  for i in range(t):
    num_to_append = (i << 8)
    c = num_to_append + ciphertext
    for column in range(1, t):
      c_t = c
      for x in range(t - 1 - column):
        c_t = num_to_append + \
          sbox_feistel_system.encrypt_block(plaintext, key=c_t)
      # for k, value in lists[i].items():
      if c_t in lists[i]:
        x_l0 = lists[i].get(c_t)
        key = x_l0
        for x in range(column - 1):
          key = num_to_append + \
            sbox_feistel_system.encrypt_block(
              plaintext, key=key)
        c_expected = num_to_append + \
          sbox_feistel_system.encrypt_block(plaintext, key=key)
        if c == c_expected:
          return key
        else:
          # If collision occurs but it is not the right key
          continue
  return False


def get_key(plaintext: int, ciphertext: int):
  original_plaintext = plaintext
  original_ciphertext = ciphertext
  block_idx = 0
  while plaintext != 0:
    plaintext_block = plaintext % (2**8)
    ciphertext_block = ciphertext % (2**8)
    key_found = get_key_block(plaintext_block, ciphertext_block, block_idx)
    if key_found != False:
      final = sbox_feistel_system.encrypt(
        original_plaintext, key=key_found)
      if original_ciphertext == int(final, 2):
        break
    plaintext = plaintext >> 8
    ciphertext = ciphertext >> 8
    block_idx += 1
    if plaintext == 0:
      return False

  return key_found


if __name__ == "__main__":
  time = datetime.now().timestamp()
  seed(int(time))

  plaintext = bytes(
    input("Please enter your plaintext\n").rstrip('\n'), encoding='utf-8')
  plaintext = int(plaintext.hex(), 16)

  # Precomutation phase begins here.
  plaintext_precomputation = plaintext
  i = 0
  while plaintext_precomputation != 0:
    plaintext_block = plaintext_precomputation % (2**8)
    block_tmto_list = compute_tmto_lists(plaintext_block)
    with open(f"block_{i}.pkl", 'wb') as f:
      pickle.dump(block_tmto_list, f)
    i += 1
    plaintext_precomputation = ( plaintext_precomputation >> 8)

  key = 2332
  original_plaintext = plaintext
  original_ciphertext = sbox_feistel_system.encrypt(
    original_plaintext, key=key)
  print(original_ciphertext)
  ciphertext = int(original_ciphertext, 2)
  print(ciphertext)
  print(f'KEY: {key}')
  block_idx = 0
  while plaintext != 0:
    plaintext_block = plaintext % (2**8)
    ciphertext_block_1 = sbox_feistel_system.encrypt_block(
      plaintext_block, key=key)
    ciphertext_block = ciphertext % (2**8)
    assert ciphertext_block == ciphertext_block_1
    key_found = get_key_block(plaintext_block, ciphertext_block, block_idx)
    if key_found != False:
      final = sbox_feistel_system.encrypt(
        original_plaintext, key=key_found)
      if original_ciphertext == final:
        break
    plaintext = plaintext >> 8
    ciphertext = ciphertext >> 8
    block_idx += 1
    if plaintext == 0:
      print("Key not found")
      exit()
  print(f"KEY FOUND {key_found}")
  ciphertext = sbox_feistel_system.encrypt(original_plaintext, key=key)
  final = sbox_feistel_system.encrypt(original_plaintext, key=key_found)

  assert(ciphertext == final)
