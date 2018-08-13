#!/usr/bin/env python

from math import sqrt

def isprime(x):
    if x == 1:
        return False
    k = int(sqrt(x))
    for j in range(2,k+1):
        if x % j == 0:
            return False
    else:
        return True

def monisen(n):
    count = 0
    x = 1
    while count != n:
        if (isprime(x)):
            t = 2**x - 1
            if isprime(t):
                print("The {} th member monisen(M) is: {}; P is {}".format(count+1, t, x))
                count += 1
        x += 1

x = int(input("Please tell me you want to know the N th monisen number?"))
monisen(x)

