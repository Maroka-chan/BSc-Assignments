import random
import hashlib

roll = random.randint(1,6)
rnd_bits = random.getrandbits(roll.bit_length())

c = str(roll) + str(rnd_bits)
commitment = hashlib.sha256(c.encode()).digest()
