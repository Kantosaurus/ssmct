from Crypto.Util.number import getPrime, bytes_to_long
from math import log2, floor

flag = "SSMCTF{??????????}" # number of ?s not necessarily accurate
secret = bytes_to_long(flag.encode('utf-8'))
bits = floor(log2(secret) + 1)

def baka(ba, ka):
    bakabaka = ba
    for bakabakabaka in range(ka-1):
        bakabaka = ba**bakabaka
    return bakabaka

def hyperbaka(ba, ka, bakabaka):
    if bakabaka == 1:
        return ba**ka
    elif ka == 0:
        return 1
    elif bakabaka == 2 and ba == ka:
        return baka(ba, bakabaka)
    else:
        bakabakabaka = hyperbaka(ba, ka-1, bakabaka)
        return hyperbaka(ba, bakabakabaka, bakabaka-1)

def triple_baka(n):
    if n == 1:
        return hyperbaka(3, 3, 4)
    else:
        return hyperbaka(3, 3, triple_baka(n-1))

TRIPLE_BAKA = triple_baka(64)

a = getPrime(bits // 2) + 1
b = getPrime(bits // 2)
x = getPrime(bits // 2)
m = getPrime(bits)

def get_next():
    global x
    x = (a * x + b) % m

print(f'{bits = }')

for i in range(1, TRIPLE_BAKA + 1):
    get_next()
    if i <= 10:
        print(i, x)

ct = secret ^ x
print(f'{ct = }')

# 1 10275910798653121436396833379154598008161
# 2 2068591239728841545706452127889450693176
# 3 26350147429806384823786121899280661716493
# 4 25358475244916002220884659082517978530071
# 5 12563752780567442975545946639227178025296
# 6 19642601882956204519785723889340847589962
# 7 6259116168994041128833294897342371591968
# 8 16406333604491605091556863399044907242384
# 9 25867766060185127305007083226436225587634
# ct = 8194779757417092844428719009359907728048