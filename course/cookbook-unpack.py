#!/usr/bin/env python

data = (1,2,3,"this is a string",(2020,8,26),["aa","bb"],6)
#num1,num2,num3,other = data #this will be wrong
num1,num2,*other,last = data #this output part of data in the middle.
#all: num1,num2,num3,other,_,_,_ = data #output all
print(other)
data_str="thisisastring"
a,b,c,d,*rest = data_str
print(rest)

record = [
    ('foo',1,2),
    ('string','hello'),
    ('foo',3,4)
]

def do_foo(x,y):
    print('do foo:',x,y)

def do_string(s):
    print('do string:',s)

for tag, *args in record:
    if tag == 'foo':
        do_foo(*args)
    elif tag == 'string':
        do_string(*args)

line = 'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false'
uname, *fields ,homedir ,sh = line.split(':')
print("Username: {}".format(uname))
print("Home dir: {}".format(homedir))
print("User shell:{}".format(sh))

