from random import randint

# Our predefined values
g = 666
p = 6661
bob_pk = 2227
message = 2000


def gen_pubkey(base, sk, prime):
    return (base ** sk) % prime

def gen_keypair(base, prime):
    sk = randint(1, prime)
    return (gen_pubkey(base, sk, prime), sk)

def encrypt(message, receiver_pk, sk, prime):
    return receiver_pk**sk % prime * message

def decrypt(ciphertext, sender_pk, sk, prime):
    return ciphertext * sender_pk**(sk * (prime-2)) % prime

def bruteforce_sk(ct, base, prime, pk):
    for sk in range(p):
        if gen_pubkey(base, sk, prime) == pk:
            break
    return sk



# Alice's Keypair
(alice_pk, alice_sk) = gen_keypair(g, p)

# Alice's Encrypted Message
ciphertext = encrypt(message, bob_pk, alice_sk, p)


# Part 1
bob_sk = bruteforce_sk(ciphertext, g, p, bob_pk)

print("1:")
print("Ciphertext: ", ciphertext)
print("Decrypted Ciphertext: ", decrypt(ciphertext, alice_pk, bob_sk, p))
print("Bob's private key: ", bob_sk)
print("\n")


# Part 2
modified_message = ciphertext * 3 % p

# (g^(xy) * m) / g^(xy) = (g^(xy) * m) * g^(xy)^-1
print("2:")
print("Ciphertext: ", ciphertext)
print("Decrypted Ciphertext", decrypt(ciphertext, alice_pk, bob_sk, p))
print("Modified Ciphertext: ", modified_message)
print("Decrypted Modified Ciphertext", decrypt(modified_message, alice_pk, bob_sk, p))



