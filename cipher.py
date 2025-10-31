
"""
Anna Prack
Affine Cipher Guessing Program
10/30/2025
"""

import random
import math
import sys

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def egcd(a, b): ##Extended GCD. Returns (g, x, y) such that a*x + b*y = g = gcd(a,b).
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m): ##Return modular inverse of a mod m, or None if none exists.
    g, x, _ = egcd(a, m)
    if g != 1:
        return None
    else:
        return x % m

def sanitize_char(c): ##Return uppercase letter index 0..25 or None for non-letter.
    if c.isalpha():
        return ord(c.upper()) - ord('A')
    return None

def affine_encrypt(plaintext, a, b):
    output = []
    for ch in plaintext:
        i = sanitize_char(ch)
        if i is None:
            output.append(ch)  #leave spaces/punctuation unchanged
        else:
            ciph_i = (a * i + b) % 26
            out_char = ALPHABET[ciph_i]
            output.append(out_char if ch.isupper() else out_char.lower()) #keep original case
    return ''.join(output)

def affine_decrypt(ciphertext, a, b):
    a_inv = modinv(a, 26)
    #if a_inv is None:
    #    raise ValueError("a has no modular inverse modulo 26")
    output = []
    for ch in ciphertext:
        i = sanitize_char(ch)
        if i is None:
            output.append(ch)
        else:
            plain_i = (a_inv * (i - b)) % 26
            out_char = ALPHABET[plain_i]
            output.append(out_char if ch.isupper() else out_char.lower()) #keep case
    return ''.join(output)

def valid_a_values(): #Return values 1..25 that are coprime to 26.
    return [x for x in range(1, 26) if math.gcd(x, 26) == 1]

def choose_random_key():
    a_choices = valid_a_values()
    a = random.choice(a_choices)
    b = random.randrange(0, 26)
    return a, b

def parse_guess(guess): #Parse a guess string like '5 8' into (a,b). Returns None if invalid.
    parts = guess.strip().split()
    if len(parts) != 2:
        return None
    try:
        a = int(parts[0])
        b = int(parts[1])
    except ValueError:
        return None
    if not (1 <= a <= 25 and 0 <= b <= 25):
        return None
    if math.gcd(a, 26) != 1:
        return None
    return a, b

def main():
    print("Anna Prack Affine Cipher")
    plaintext = input("Enter the plaintext to encrypt: ").rstrip("\n")

    # choose a hidden key
    a_secret, b_secret = choose_random_key()
    ciphertext = affine_encrypt(plaintext, a_secret, b_secret)

    print("Encrypted!")
    print(ciphertext)
    print("To guess, enter two integers (\"a b\" format)")
    print("(a must be between 1-25 and gcd with 26 must be 1)")
    print("(b must be between 0-25)")

    while True:
        guess = input(f"New Guess (a, b): ").strip()
        if guess.lower() == "reveal":
            print(f"Key was a={a_secret}, b={b_secret}")
            print("Entered plaintext:", affine_decrypt(ciphertext, a_secret, b_secret))
            break

        parsed = parse_guess(guess)
        if parsed is None:
            print("Invalid format")
            print("Enter two integers (\"a b\" format)")
            print("(a must be between 1-25 and gcd with 26 must be 1)")
            print("(b must be between 0-25)")
            continue

        a_guess, b_guess = parsed
        if (a_guess, b_guess) == (a_secret, b_secret):
            print("\nCorrect!")
            print("Decrypted plaintext:", affine_decrypt(ciphertext, a_guess, b_guess))
            break
        else:
            print("Incorrect. Try again.\n")

if __name__ == "__main__":
        main()