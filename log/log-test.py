#!/usr/bin/env python

from logger import create_logger
import os

#Usage: 
logname = os.path.basename(__file__).replace(".py","",1)  #this filename log-test
LOGGER = create_logger(app_name=logname,level='DEBUG')

def yxtest1():
    LOGGER.info("Running %d", 1)

def yxtest2():
    LOGGER.warning("Running %s", 2)

def yxtest3():
    LOGGER.error("Running %s", 3)

def yxtest4():
    LOGGER.critical("Running %s", 4)

def main():
    LOGGER.debug("Running %03d", 0)
    yxtest1()
    yxtest2()
    yxtest3()
    yxtest4()

if __name__ == "__main__":
   main()
   