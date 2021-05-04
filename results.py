import matplotlib.pyplot as plt
from tmto import get_key, m, t, compute_tmto_lists
import time
import numpy as np
import pickle

chosen_plaintext = int(b'Hello'.hex(), 16)
ciphertext_part = int(b'\x82K\xc1\xc1\x9d'.hex(),16)



def m_precompute_time():
    for i in range(7):
        m = 2**(i)
        plaintext_precomputation = chosen_plaintext
        x_axis.append(m)
        block_idx = 0
        start = time.time()
        while plaintext_precomputation != 0:
            plaintext_block = plaintext_precomputation % (2**8)
            block_tmto_list = compute_tmto_lists(plaintext_block, m)
            
            block_idx += 1
            plaintext_precomputation = ( plaintext_precomputation >> 8)
        end = time.time()

        y_axis.append(end-start)

    print(x_axis, y_axis)
    plt.plot(np.array(x_axis), np.array(y_axis))
    plt.xlabel("number of rows in list")
    plt.ylabel("miliseconds")
    # plt.show()
    plt.savefig('m-precompute.png')

def t_precompute_time():
    for i in range(7):
        m = 2**(i)
        plaintext_precomputation = chosen_plaintext
        x_axis.append(m)
        block_idx = 0
        start = time.time()
        while plaintext_precomputation != 0:
            plaintext_block = plaintext_precomputation % (2**8)
            block_tmto_list = compute_tmto_lists(plaintext_block, m)
            
            block_idx += 1
            plaintext_precomputation = ( plaintext_precomputation >> 8)
        end = time.time()

        y_axis.append(end-start)

    print(x_axis, y_axis)
    plt.plot(np.array(x_axis), np.array(y_axis))
    plt.xlabel("Number of columns in list")
    plt.ylabel("Time (in milliseconds)")
    # plt.show()
    plt.savefig('t-precompute-time.png')

def t_precompute_size():
    for i in range(7):
        m = 2**(i)
        plaintext_precomputation = chosen_plaintext
        x_axis.append(m)
        block_idx = 0
        start = time.time()
        while plaintext_precomputation != 0:
            plaintext_block = plaintext_precomputation % (2**8)
            block_tmto_list = compute_tmto_lists(plaintext_block, m)
            
            block_idx += 1
            plaintext_precomputation = ( plaintext_precomputation >> 8)
        end = time.time()
        y_axis.append(len(block_tmto_list))

    print(x_axis, y_axis)
    plt.plot(np.array(x_axis), np.array(y_axis))
    plt.xlabel("Number of columns in list")
    plt.ylabel("Number of elements in list")
    # plt.show()
    plt.savefig('t-precompute-size.png')


# t_precompute_time()
# t_precompute_size()
# x = np.array(range(64))
# y = 2*x*(2**4)
# plt.plot(x, y)
# plt.xlabel("Number of columns in list")
# plt.ylabel("Number of elements in list")
# # plt.show()
# plt.savefig('t-precompute-size.png')

# plt.xlabel("Number of rows in list")
# plt.ylabel("Number of elements in list")
# plt.savefig('m-precompute-size.png')

def t_online_time():
    x_axis = list()
    y_axis = list()
    for i in range(8):
        
        m = 2**(i)
        plaintext_precomputation = chosen_plaintext
        x_axis.append(m)
        block_idx = 0
        while plaintext_precomputation != 0:
            plaintext_block = plaintext_precomputation % (2**8)
            block_tmto_list = compute_tmto_lists(plaintext_block, m)
            with open(f"block_{block_idx}.pkl", 'wb') as f:
                pickle.dump(block_tmto_list, f)
            block_idx += 1
            plaintext_precomputation = ( plaintext_precomputation >> 8)

        start_time = time.time()
        key_found = get_key(chosen_plaintext, ciphertext_part)
        end_time = time.time()
        print(key_found, i)
        y_axis.append(end_time - start_time)

    print(x_axis, y_axis)
    plt.plot(np.array(x_axis), np.array(y_axis))
    plt.xlabel("Number of columns in list")
    plt.ylabel("Time (in milliseconds)")
    # plt.show()
    plt.savefig('t-online-time.png')

def m_online_time():
    x_axis = list()
    y_axis = list()
    for i in range(8):
        
        m = 2**(i)
        plaintext_precomputation = chosen_plaintext
        x_axis.append(m)
        block_idx = 0
        while plaintext_precomputation != 0:
            plaintext_block = plaintext_precomputation % (2**8)
            block_tmto_list = compute_tmto_lists(plaintext_block, m)
            with open(f"block_{block_idx}.pkl", 'wb') as f:
                pickle.dump(block_tmto_list, f)
            block_idx += 1
            plaintext_precomputation = ( plaintext_precomputation >> 8)

        start_time = time.time()
        key_found = get_key(chosen_plaintext, ciphertext_part)
        end_time = time.time()
        print(key_found, i)
        y_axis.append(end_time - start_time)

    print(x_axis, y_axis)
    plt.plot(np.array(x_axis), np.array(y_axis))
    plt.xlabel("Number of rows in list")
    plt.ylabel("Time (in milliseconds)")
    # plt.show()
    plt.savefig('m-online-time-2.png')

m_online_time()
# t_online_time()
