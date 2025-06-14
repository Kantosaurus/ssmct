from Crypto.Util.number import bytes_to_long
import os

class Random():
    def __init__(self, seed=None):
        if seed == None:
            self.seed = os.urandom(32*2//8)
        else:
            self.seed == seed
        if type(self.seed) == bytes:
            self.seed = bytes_to_long(self.seed)
        self.state = 0xdeadbeef00c0ffee
        self.pos = 0
        self.tempers = [self.temper1,self.temper2,self.temper3,self.temper4]
    
    def temper1(self,y):
        for _ in range(5):
            y ^= (y >> 12)
            y ^= (y << 31) & 0x95fa54741af72bd
            y ^= (y << 27) & 0xdf2a12b81bbaaa21
            y ^= (y >> 5)
        return y

    def temper2(self, y):
        for _ in range(5):
            y ^= (y >> 6)
            y ^= (y << 45) & 0x93b619c288a727f2
            y ^= (y << 21) & 0xb4ef30c811f03be3
            y ^= (y >> 4)
        return y

    def temper3(self, y):
        for _ in range(5):
            y ^= (y >> 15)
            y ^= (y << 37) & 0xa9abc7ad872eb501
            y ^= (y << 28) & 0xdad65256c7af43dd
            y ^= (y >> 5)
        return y

    def temper4(self, y):
        for _ in range(5):
            y ^= (y >> 10)
            y ^= (y << 5) & 0xb475d401139b1ae0
            y ^= (y << 8) & 0x79a2d936fe0515c3
            y ^= (y >> 3)
        return y

    
    def gen(self):
        curr = 0b11 << ((self.pos % 32)*2)
        curr &= self.seed
        curr >>= ((self.pos % 32)*2)
        self.pos += 1
        self.state = self.tempers[curr](self.state)
        return self.state

