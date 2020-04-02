#!/usr/bin/env python

import logging

def create_logger(app_name=None, level='WARNING'):
    logger = logging.getLogger(app_name or __name__)
    logger.setLevel(level)
    log_format = '[%(asctime)-15s] [%(levelname)08s] [%(filename)s] (%(funcName)s) %(message)s'
    logging.basicConfig(format=log_format, datefmt='%Y-%m-%d %H:%M:%S')
    return logger

def main():
    LOGGER = create_logger(level='DEBUG')
    LOGGER.debug("Running: %d", 0)

if __name__ == "__main__":
    main()
