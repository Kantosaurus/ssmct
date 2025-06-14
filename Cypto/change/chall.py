from PRNG import Random
from hashlib import sha256
from Crypto.Util.number import long_to_bytes

random = Random()

hints = []
for i in range(32):
    hints.append(random.gen())
print(f'{hints = }')

prev = hints[-1]
for i in range(32,2**100):
    curr = random.gen()
    if curr == prev ^ 1: # I do love a low rate of change
        break
    prev = curr
    

flag = "SSMCTF{%s}"%sha256(long_to_bytes(i)).hexdigest()
print(flag)