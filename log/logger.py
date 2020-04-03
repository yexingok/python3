#!/usr/bin/env python

import logging
import os

def create_logger(app_name=None, level='warning', path='logs/'):
    # parm app_name (requried): application name
    # parm level: loglevel; details see: https://docs.python.org/3/howto/logging.html 
    # parm path: logs path; logs will be writes to this path with specified app_name.
    # return: stream logger obj
    logger = logging.getLogger(app_name)
    logger.setLevel(level.upper())
        
    # Add stream handler, output all level
    streamhd = logging.StreamHandler()
    streamhd.setLevel(logging.DEBUG)
    log_format = '[%(asctime)-15s] [%(levelname)08s] [%(filename)s] (%(funcName)s) (line: %(lineno)d): %(message)s'
    formatter = logging.Formatter(fmt=log_format, datefmt='%Y-%m-%d %H:%M:%S')
    streamhd.setFormatter(formatter)
    logger.addHandler(streamhd)

    # Add same format file handler, log warning and above level:
    # Caller should specifiy app_name,
    thisfile = os.path.basename(__file__).replace(".py","",1)
    if app_name != thisfile and app_name:
        if not os.path.isdir(path):
            os.mkdir(path)
        filehd = logging.FileHandler(filename=path+app_name+'.log', mode='w' ,encoding='utf-8')
        filehd.setLevel(logging.WARNING)
        filehd.setFormatter(formatter)
        logger.addHandler(filehd)
    return logger

def main():
    # Sample Usage: (put in actual file)
    logfile = os.path.basename(__file__).replace(".py","",1)
    LOGGER = create_logger(app_name=logfile, level='DEBUG')
    LOGGER.debug("Running: %d", 0)

if __name__ == "__main__":
    main()
