import sys
import os
# To access to my module or use a virtual env and comment the line below
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cryptage.crypting import *

#performance test
import time 
public_key, private_key = generate_rsa_keys(bits=1024)  # RSA-1024 (because n = 1024 bits)


message = "bonjour tout le monde"
msg = int.from_bytes(message.encode('utf-8'), 'big')
n, e = public_key

start = time.time()
pow(msg, e, n)
end = time.time()  


""" st2 = time.time()
#fastExp(msg,intToBinExp(e)) % n
public_key, private_key = generate_rsa_keys()
en2 = time.time()

print(end - start)
print(en2 - st2) """

########### test #########""
""" msg_test = "bonjour le monde"
msg_code = encrypt_rsa(msg_test, public_key)
print("voici le msg crypte : " , msg_code)

msg_dec = decrypt_rsa(msg_code, private_key)
print("voici le msg decrypte : " , msg_dec) 

#cle public 
print("voici ma cle public : " , public_key) """
