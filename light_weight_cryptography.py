SBOX_TABLE = [
    0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
    0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2
]

INVERSE_SBOX_TABLE = [
    0x5, 0xE, 0xF, 0x8, 0xC, 0x1, 0x2, 0xD,
    0xB, 0x4, 0x6, 0x3, 0x0, 0x7, 0x9, 0xA
]

PERMUTATION_BOX = [
    0, 16, 32, 48, 1, 17, 33, 49,
    2, 18, 34, 50, 3, 19, 35, 51,
    4, 20, 36, 52, 5, 21, 37, 53,
    6, 22, 38, 54, 7, 23, 39, 55,
    8, 24, 40, 56, 9, 25, 41, 57,
    10, 26, 42, 58, 11, 27, 43, 59,
    12, 28, 44, 60, 13, 29, 45, 61,
    14, 30, 46, 62, 15, 31, 47, 63
]

INVERSE_PERMUTATION_BOX = [PERMUTATION_BOX.index(i) for i in range(64)]

def apply_sbox(input_state):
    result = 0
    for i in range(16):
        nibble = (input_state >> (i * 4)) & 0xF
        result |= SBOX_TABLE[nibble] << (i * 4)
    return result

def reverse_sbox(input_state):
    result = 0
    for i in range(16):
        nibble = (input_state >> (i * 4)) & 0xF
        result |= INVERSE_SBOX_TABLE[nibble] << (i * 4)
    return result

def apply_permutation(input_state):
    result = 0
    for i in range(64):
        bit = (input_state >> i) & 1
        result |= bit << PERMUTATION_BOX[i]
    return result

def reverse_permutation(input_state):
    result = 0
    for i in range(64):
        bit = (input_state >> i) & 1
        result |= bit << INVERSE_PERMUTATION_BOX[i]
    return result

def xor_key(input_state, key):
    return input_state ^ key

def generate_round_key(init_key, round_number):
    round_key = (init_key >> 16) & 0xFFFFFFFFFFFFFFFF
    init_key = ((init_key << 61) | (init_key >> 19)) & ((1 << 80) - 1)
    sbox_output = SBOX_TABLE[(init_key >> 76) & 0xF]
    init_key = (init_key & ~(0xF << 76)) | (sbox_output << 76)
    init_key ^= round_number << 15
    return round_key, init_key

def encrypt(plaintext, key):
    state = plaintext
    for round_number in range(1, 32):
        round_key, key = generate_round_key(key, round_number)
        state = xor_key(state, round_key)
        state = apply_sbox(state)
        state = apply_permutation(state)
    round_key, _ = generate_round_key(key, 32)
    state = xor_key(state, round_key)
    return state

def decrypt(ciphertext, key):
    state = ciphertext
    round_keys = []
    temp_key = key
    for round_number in range(1, 33):
        round_key, temp_key = generate_round_key(temp_key, round_number)
        round_keys.append(round_key)

    round_keys.reverse()
    state = xor_key(state, round_keys[0])
    for round_key in round_keys[1:]:
        state = reverse_permutation(state)
        state = reverse_sbox(state)
        state = xor_key(state, round_key)
    return state

if __name__ == "__main__":
    plaintext = 0x0123456789ABCDEF
    key = 0x0123456789ABCDEFFEDCBA9876543210
    print(f"Original Plaintext: {plaintext:016X}")
    ciphertext = encrypt(plaintext, key)
    print(f"Encrypted Ciphertext: {ciphertext:016X}")
    decrypted = decrypt(ciphertext, key)
    print(f"Decrypted Text: {decrypted:016X}")
