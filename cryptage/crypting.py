import random
from sympy import mod_inverse, isprime


# function: decompose an integer into a sum of powers of 2
# input: int
# output: list of int
# result: list of exponents of 2 in our sum
def intToBinExp(num):
    binNum = bin(num)
    l = []
    for i in range(2,len(binNum)):
        if binNum[i] == "1":
            l.append(len(binNum) - 1 - i )
    return l

# fonction : calcculatean integer to the power of an other integer
# with the algorythm of fast exponentielle
# input : int , int list
# output : int
# result : the integer to the power of an other (with specific format : see intToBinExp )
def fastExp(c,lexp):
    res = 1
    lexp.reverse()
    for i in lexp:
         if i == 0:
            res *= c
         else:
            # (c ^ (2 ^ (i - 1))) ^ 2
            res *= (c ** (2 ** (i - 1))) ** 2
    return res



# Générer un nombre premier d'une taille donnée en bits
def generate_large_prime(bits):
    while True:
        # Générer un nombre aléatoire de la taille spécifiée en bits
        prime_candidate = random.getrandbits(bits)
        # S'assurer que le nombre est impair
        prime_candidate |= (1 << bits - 1) | 1
        # Vérifier s'il est premier
        if isprime(prime_candidate):
            return prime_candidate

# Génération des clés RSA avec de grands nombres premiers
def generate_rsa_keys(bits=1024):
    # Choisir deux grands nombres premiers p et q
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Choisir un exposant public e (65537 est souvent utilisé)
    e = 65537

    # Calculer l'exposant privé d (l'inverse de e modulo phi_n)
    d = mod_inverse(e, phi_n)

    # Clé publique (n, e), clé privée (n, d)
    return (n, e), (n, d)

public_key, private_key = generate_rsa_keys(bits=1024)  # RSA-2048 (car n sera de 2048 bits)
print("Public Key:", public_key)
print("Private Key:", private_key)


###########################################################################################

# Fonction pour chiffrer un message (message doit être un entier)
def encrypt_rsa(message, public_key):
    n, e = public_key
    return pow(message, e, n)  # message^e % n

# Fonction pour déchiffrer un message chiffré
def decrypt_rsa(cipher, private_key):
    n, d = private_key
    return pow(cipher, d, n)  # cipher^d % n

# Message à chiffrer
message = 123  # Le message doit être converti en entier

# Chiffrement
cipher = encrypt_rsa(message, public_key)
print("Chiffrement:", cipher)

# Déchiffrement
decrypted_message = decrypt_rsa(cipher, private_key)
print("Déchiffrement:", decrypted_message)

