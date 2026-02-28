import logging
import sys 
import time


def setupLogger(programName):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(f'{programName}_{int(time.time())}.log')
        ]
    )


def getLogger(name: str) -> logging.Logger:
    return logging.Logger(name)