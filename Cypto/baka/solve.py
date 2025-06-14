from Crypto.Util.number import long_to_bytes

# First 10 outputs
outputs = [
    10275910798653121436396833379154598008161,
    2068591239728841545706452127889450693176,
    26350147429806384823786121899280661716493,
    25358475244916002220884659082517978530071,
    12563752780567442975545946639227178025296,
    19642601882956204519785723889340847589962,
    6259116168994041128833294897342371591968,
    16406333604491605091556863399044907242384,
    25867766060185127305007083226436225587634
]

ct = 8194779757417092844428719009359907728048

def crack_lcg(ys):
    from math import gcd
    from functools import reduce
    ds = [ys[i+1] - ys[i] for i in range(len(ys)-1)]
    zs = [ds[i+1] * ds[i-1] - ds[i] * ds[i] for i in range(1, len(ds)-1)]
    m = abs(reduce(gcd, zs))
    return m

m = crack_lcg(outputs)
print(f"[+] Recovered modulus m: {m}")

x0 = outputs[0]
x9 = outputs[8]  # Start from last known output

delta1 = (outputs[1] - outputs[0]) % m
delta2 = (outputs[2] - outputs[1]) % m

a = (delta2 * pow(delta1, -1, m)) % m
b = (outputs[1] - a * outputs[0]) % m

print(f"[+] Recovered a: {a}")
print(f"[+] Recovered b: {b}")

# Define LCG step
def step(x):
    return (a * x + b) % m

# Try up to 100,000 steps from x9
x = x9
for i in range(100_000):
    x = step(x)
    candidate = x ^ ct
    flag_candidate = long_to_bytes(candidate).decode('utf-8', errors='ignore')
    if 'SSMCTF{' in flag_candidate:
        print(f"\n[+] Found possible flag at step {i+1} (after x9):")
        print(f"    Flag: {flag_candidate}")
        break
else:
    print("[!] No flag found in 100,000 steps after x9")