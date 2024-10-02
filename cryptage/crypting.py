import random
from sympy import mod_inverse, isprime
import threading
import queue
import time

def generate_large_prime(bits, output_queue):
    while True:
        prime_candidate = random.getrandbits(bits)
        prime_candidate |= (1 << bits - 1) | 1  # To verify if the number is odd
        if isprime(prime_candidate):
            output_queue.put(prime_candidate)  # Add the result in the queue
            break

# Generate RSA keys with default size of 1024 bits
def generate_rsa_keys(bits=2048):
    q = queue.Queue()

    # To have two threads for calculate 2 prime number (much faster)
    thread1 = threading.Thread(target=generate_large_prime, args=(bits, q))
    thread2 = threading.Thread(target=generate_large_prime, args=(bits, q))

    start = time.time()
    thread1.start()
    thread2.start()

    # Get results in the queue
    p = q.get()  # waiting for the value 
    en1 = time.time()
    qp = q.get()
    en2 = time.time()

    thread1.join()
    thread2.join()
    n = p * qp
    phi_n = (p - 1) * (qp - 1)

    # Public exposant e (65537 is often chosen)
    e = 65537

    #formula (e * d) mod phi(n) = 1 
    #So if we want d with n and e known => d = mod_inverse (e, phi_n)
    # Calculer l'exposant privé d (l'inverse de e modulo phi_n)
    d = mod_inverse(e, phi_n)

    # Clé publique (n, e), clé privée (n, d)
    return (n, e), (n, d)

# Function to encrypt (must be an integer)
def encrypt_rsa(message, public_key):

    #convert string into int ( necessary )
    msg = int.from_bytes(message.encode('utf-8'), 'big')
    n, e = public_key
    #pow is very powerful, much more so than our functions due to its low-level implementation
    return pow(msg, e, n)  # message ** e % n

# Function to decrypt
def decrypt_rsa(cipher, private_key):
    n, d = private_key
    msg_dec = pow(cipher, d, n)  # cipher ** d % n
    return msg_dec.to_bytes((msg_dec.bit_length() + 7) // 8, 'big').decode('utf-8')

