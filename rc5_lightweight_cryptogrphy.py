def rotate_left(val, shift, word_size=32):
    return ((val << shift) & (2**word_size - 1)) | (val >> (word_size - shift))


def rotate_right(val, shift, word_size=32):
    return ((val >> shift) | (val << (word_size - shift))) & (2**word_size - 1)


def generate_keys(secret_key, word_size=32, rounds=12):
    """RC5 Key Expansion."""
    bytes_in_word = word_size // 8
    key_length = len(secret_key)
    num_words = max(1, (key_length + bytes_in_word - 1) // bytes_in_word)
    key_words = [0] * num_words
    for i in range(key_length):
        key_words[i // bytes_in_word] = (
            key_words[i // bytes_in_word] << 8
        ) + secret_key[i]

    P_const = 0xB7E15163
    Q_const = 0x9E3779B9
    key_schedule = [
        (P_const + i * Q_const) & (2**word_size - 1) for i in range(2 * (rounds + 1))
    ]

    i = j = A = B = 0
    for _ in range(3 * max(num_words, 2 * (rounds + 1))):
        A = key_schedule[i] = rotate_left(
            (key_schedule[i] + A + B) & (2**word_size - 1), 3, word_size
        )
        B = key_words[j] = rotate_left(
            (key_words[j] + A + B) & (2**word_size - 1),
            (A + B) & (word_size - 1),
            word_size,
        )
        i = (i + 1) % (2 * (rounds + 1))
        j = (j + 1) % num_words
    return key_schedule


def rc5_encrypt_block(plaintext_block, key_schedule, word_size=32, rounds=12):
    """RC5 Block Encryption."""
    A = int.from_bytes(plaintext_block[:4], "little")
    B = int.from_bytes(plaintext_block[4:], "little")
    A = (A + key_schedule[0]) & (2**word_size - 1)
    B = (B + key_schedule[1]) & (2**word_size - 1)
    for i in range(1, rounds + 1):
        A = (
            rotate_left((A ^ B), B & (word_size - 1), word_size) + key_schedule[2 * i]
        ) & (2**word_size - 1)
        B = (
            rotate_left((B ^ A), A & (word_size - 1), word_size)
            + key_schedule[2 * i + 1]
        ) & (2**word_size - 1)

    return A.to_bytes(4, "little") + B.to_bytes(4, "little")


def rc5_decrypt_block(ciphertext_block, key_schedule, word_size=32, rounds=12):
    """RC5 Block Decryption."""
    A = int.from_bytes(ciphertext_block[:4], "little")
    B = int.from_bytes(ciphertext_block[4:], "little")
    for i in range(rounds, 0, -1):
        B = (
            rotate_right(
                (B - key_schedule[2 * i + 1]) & (2**word_size - 1),
                A & (word_size - 1),
                word_size,
            )
            ^ A
        )
        A = (
            rotate_right(
                (A - key_schedule[2 * i]) & (2**word_size - 1),
                B & (word_size - 1),
                word_size,
            )
            ^ B
        )

    B = (B - key_schedule[1]) & (2**word_size - 1)
    A = (A - key_schedule[0]) & (2**word_size - 1)
    return A.to_bytes(4, "little") + B.to_bytes(4, "little")


if __name__ == "__main__":
    secret_key = b"this_is_a_16_byte_key"
    plaintext_block = b"12345678"
    print(f"Original Plaintext: {plaintext_block.decode()}")

    if len(secret_key) < 1:
        raise ValueError("Key length must be at least 1 byte.")

    key_schedule = generate_keys(secret_key)

    ciphertext_block = rc5_encrypt_block(plaintext_block, key_schedule)
    print("Encrypted Ciphertext (Hex):", ciphertext_block.hex())

    decrypted_block = rc5_decrypt_block(ciphertext_block, key_schedule)
    print("Decrypted Plaintext:", decrypted_block.decode())
