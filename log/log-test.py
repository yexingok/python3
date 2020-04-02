#!/usr/bin/env python

from logger import create_logger

LOGGER = create_logger(level='DEBUG')

def yxtest1():
    LOGGER.info("Running %d", 1)

def yxtest2():
    LOGGER.error("Running %s", 2)

def main():
    LOGGER.debug("Running %03d", 0)
    yxtest1()
    yxtest2()

if __name__ == "__main__":
   main()
