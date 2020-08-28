#!/usr/bin/env python

def frange(start, stop, increment):
    x = start
    while(x < stop):
        yield x
        x += increment

for n in frange(1, 10, 0.5):
    print(n)

def fab1(max):
    n, a, b = 0, 0, 1
    L = []
    while(n < max):
        L.append(b)
        a, b = b, a + b
        n += 1
    return L

L = fab1(5)
print(L)
