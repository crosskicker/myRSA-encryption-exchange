import random
from sympy import mod_inverse, isprime

# Generate a large prime number with a bit size given
def generate_large_prime(bits):
    while True:
        prime_candidate = random.getrandbits(bits)
        #Verify that the number is odd
        prime_candidate |= (1 << bits - 1) | 1
        #Verify is the number is a prime number
        if isprime(prime_candidate):
            return prime_candidate

# Generate RSA keys with default size of 1024 bits
def generate_rsa_keys(bits=1024):
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Public exposant e (65537 is often chosen)
    e = 65537

    #formula (e * d) mod phi(n) = 1 
    #So if we want d with n and e known => d = mod_inverse (e, phi_n)
    # Calculer l'exposant privé d (l'inverse de e modulo phi_n)
    d = mod_inverse(e, phi_n)

    # Clé publique (n, e), clé privée (n, d)
    return (n, e), (n, d)

public_key, private_key = generate_rsa_keys(bits=1024)  # RSA-2048 (car n sera de 2048 bits)
""" print("Public Key:", public_key)
print("Private Key:", private_key) """


# Function to encrypt (must be an integer)
def encrypt_rsa(message, public_key):

    #convert string into int ( necessary )
    msg = int.from_bytes(message.encode('utf-8'), 'big')
    n, e = public_key
    #pow is very powerful, much more so than our functions due to its low-level implementation
    return pow(msg, e, n)  # message^e % n

# Function to decrypt
def decrypt_rsa(cipher, private_key):
    n, d = private_key
    msg_dec = pow(cipher, d, n)  # cipher^d % n
    return msg_dec.to_bytes((msg_dec.bit_length() + 7) // 8, 'big').decode('utf-8')

