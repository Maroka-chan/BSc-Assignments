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
    return (ciphertext * (((sender_pk**sk) ** (prime-2)) % prime) % prime)

def bruteforce_sk(ct, base, prime, pk):
    sk = 1
    while sk < p:
        Bpk = (base**sk) % prime
        if Bpk == pk:
            break
        sk += 1
    return sk

def modify_message(ciphertext, prime):
    return (ciphertext * 3) % prime


ciphertext = encrypt(message_from_alice, Bob_pk, Alice_sk, p)

print("1:")
print("Ciphertext: ", ciphertext)
Bob_sk = bruteforce_sk(ciphertext, g, p, Bob_pk)
print("Decrypted Ciphertext: ", decrypt(ciphertext, Alice_pk, Bob_sk, p))
print("Bob's private key: ", Bob_sk)
print("\n")

# (g^(xy) * m) / g^(xy) = (g^(xy) * m) * g^(xy)^-1
print("2:")
print("Ciphertext: ", ciphertext)
print("Decrypted Ciphertext", decrypt(ciphertext, Alice_pk, Bob_sk, p))
modified_message = modify_message(ciphertext, p)
print("Modified Ciphertext: ", modified_message)
print("Decrypted Modified Ciphertext", decrypt(modified_message, Alice_pk, Bob_sk, p))



