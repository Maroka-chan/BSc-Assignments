from random import randint
from math import log

g = 666
p = 6661

Bob_pk = 2227

Alice_sk = randint(1,p)
Alice_pk = (g**Alice_sk) % p
message_from_alice = 2000

def encrypt(message, receiver_pk, sk, prime):
    return ((receiver_pk**sk) % prime) * message

def decrypt(ciphertext, sender_pk, sk, prime):
    return ciphertext // ((sender_pk**sk) % prime)

def bruteforce_sk(ct, base, prime, pk):
    sk = 1
    while sk < p:
        Bpk = (base**sk) % prime
        if Bpk == pk:
            break
        sk += 1
    return sk

ciphertext = encrypt(message_from_alice, Bob_pk, Alice_sk, p)
print("Ciphertext: ", ciphertext)

Bob_sk = bruteforce_sk(ciphertext, g, p, Bob_pk)
print("Decrypted Ciphertext: ", decrypt(ciphertext, Alice_pk, Bob_sk, p))
print("Bob's private key: ", Bob_sk)

