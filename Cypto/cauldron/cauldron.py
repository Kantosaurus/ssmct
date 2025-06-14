from secret import flag

def C(text):
    ...

def B(text):
    ...

def R(text):
    ...

def S(text):
    ...

def X(text):
    ...

def O(text):
    ...


text = "Double, double, toil and trouble. Fire burn and cauldron bubble!"
functions = [C, B, R, S, X, O]

output = open('output.txt', 'w')

for func1 in functions:
    for func2 in functions:
        for func3 in functions:
            output.write(func1(func2(func3(text))))
            output.write('\n')

for func in functions:
    flag = func(flag)

output.write(flag)
output.close       