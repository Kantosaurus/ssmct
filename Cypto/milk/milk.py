from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
import random

class EC:
    def __init__(self, a, b, p):
        self.a = a 
        self.b = b 
        self.p = p 
    
    # the double-and-add is implemented correctly
    def add(self, P, Q):
        if P is None:
            return Q
        if Q is None:
            return P
        
        x1, y1 = P
        x2, y2 = Q
        
        if x1 == x2 and y1 != y2:
            return None
        
        if P == Q:
            lam = (3 * x1**2 + self.a) * pow(2 * y1, -1, self.p) % self.p
        else:
            lam = (y2 - y1) * pow(x2 - x1, -1, self.p) % self.p
        
        x3 = (lam**2 - x1 - x2) % self.p
        y3 = (lam * (x1 - x3) - y1) % self.p
        
        return (x3, y3)
    
    def multiply(self, P, n):
        R = None  
        Q = P
        
        while n:
            if n & 1:
                R = self.add(R, Q)
            Q = self.add(Q, Q)
            n >>= 1
        
        return R

    def get_random_point(self):
        import random
        
        while True:
            p = self.p
            x = random.randint(0, p - 1)
            
            n = (pow(x, 3, self.p) + self.a * x + self.b) % p
            
            if pow(n, (p - 1) // 2, p) != 1:
                continue

            # don't freak out this is just tonelli shanks and it is indeed implemented properly

            q, s = p - 1, 0
            while q % 2 == 0:
                q //= 2
                s += 1
            z = 2

            while pow(z, (p - 1) // 2, p) == 1:
                z += 1

            m, c, t, r = s, pow(z, q, p), pow(n, q, p), pow(n, (q + 1) // 2, p)
            while t != 1:
                i, temp = 0, t
                while temp != 1:
                    temp = pow(temp, 2, p)
                    i += 1
                b = pow(c, 2 ** (m - i - 1), p)
                m, c, t, r = i, (b * b) % p, (t * b * b) % p, (r * b) % p
            y = r
            return (x, y)


# secure, standard curves used very often in ECC
# the parameters are all correct, if you want to check them
curve_25519_p = 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffed
curve_25519_a = 0x76d06
curve_25519_b = 0x01

M_221_p = 0x1FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD
M_221_a = 0x01c93a
M_221_b = 0x01


curve_25519 = EC(curve_25519_a, curve_25519_b, curve_25519_p)
M_221 = EC(M_221_a, M_221_b, M_221_p)

G1 = curve_25519.get_random_point()
G2 = M_221.get_random_point()

k = getPrime(200)

pt1, pt2 = curve_25519.multiply(G1, k), M_221.multiply(G2, k)

# flag encryption
import hashlib, os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from secret import FLAG

def encrypt_flag(secret: int):
    sha1 = hashlib.sha1()
    sha1.update(str(secret).encode('ascii'))
    key = sha1.digest()[:16]
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(FLAG, 16))
    return iv.hex(), ciphertext.hex()

iv, ct = encrypt_flag(k)

print(f'{G1 = }\n{G2 = }')
print(f'{pt1 = }\n{pt2 = }')
print(f'{iv = }, {ct = }')

#G1 = (47063170801806052288146673528871417153526850064394483981146410830175982208544, 53518176899357161526249489715124114639791104549020667616657543916324221249348)
#G2 = (44463004732374493397893178641833179486751816974247573994673798864, 1106794713284151358838640453450775713656116663772692522843863128471)
#pt1 = (56710714175061483991870664898200691885016604747806913517177632746453560406455, 22183016490403262414869646241566186015038886824498859131560775826194154678831)
#pt2 = (861801353887926730429905301581104022799000762265859378776929570795, 2414525705848701236524399200022909146362752492100235869363750117869)
#iv = 'c001a9fe49c5eaee271777f7deac8eb8', ct = '12068639a25f527caf97b8f8572723571ebf212cf673e71b5e705f99404cc50e97a5dbbde566ea52fde3bf8caaede3629ede5731bb4340c27a6b352636546f02'