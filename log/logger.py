#!/usr/bin/env python

import logging
import os

def create_logger(app_name=__name__, level='warning', path='logs/'):
    # parm app_name:   application name, default to this filename (os.path.basename(__file__).replace(".py","",1)) or __main__
    #                                  depends call from outside or direct call within the file
    # parm level:      loglevel; details see: https://docs.python.org/3/howto/logging.html 
    # parm path:       logs path; logs will be writes to this path with specified app_name.
    # return:          logger obj (with steam(debug) and file(warning) handler)
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
    if app_name != "__main__":
        if not os.path.isdir(path):
            os.mkdir(path)
        filehd = logging.FileHandler(filename=path+app_name+'.log', mode='a' ,encoding='utf-8')
        filehd.setLevel(logging.WARNING)
        filehd.setFormatter(formatter)
        logger.addHandler(filehd)
    return logger

def main():
    # Sample Usage: (put in actual file)
    LOGGER = create_logger(level='DEBUG')
    LOGGER.debug("Running: %d", 0)

if __name__ == "__main__":
    main()
