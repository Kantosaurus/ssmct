#!sage
from sage.all import EllipticCurve, GF
from Crypto.Util.number import bytes_to_long

flag = b'SSMCTF{REDACTED}'

#secp256k1
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0
b = 7

E = EllipticCurve(GF(p),(a,b))

A = [E.random_point() for _ in range(42)]
enc = []

m = bin(bytes_to_long(flag))[2:]
m = m.zfill(len(m)//42*42+42)

for i in range(0,len(m),42):
    buffer = None
    for j, bit in enumerate(m[i:i+42]):
        if bit == '1':
            if not buffer:
                buffer = A[j]
            else:
                buffer += A[j]
    enc.append(buffer)

A = [i.xy() for i in A]
enc = [i.xy() for i in enc]
print(f'{A = }')
print(f'{enc = }')