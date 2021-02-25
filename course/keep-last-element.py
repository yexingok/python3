#!/usr/bin/env python

import os
from collections import deque

def search(lines, pattern, history=5):
    previous_lines = deque(maxlen=history)
    for line in lines:
        if pattern in line:
            yield line, previous_lines
        previous_lines.append(line)

# Example use on a file:

if __name__ == '__main__':
    path = os.getcwd()
    with open(path + '.\course\iteration.py',"r") as f:
        for line, previous_lines in search(f,'for',5):
            for pline in previous_lines:
                print(pline, end='')
            print(line, end='')
            print('-'*20)

