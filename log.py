import os
from datetime import datetime


class FileLog:
    def __init__(self, LOG_DIR):
        self.LOG_DIR = LOG_DIR

    def log(self, str):
        LOG_FILE = open(os.path.join(self.LOG_DIR, 'log.txt'), 'a')

        current_time = datetime.now().strftime("%H:%M:%S")
        logStr = current_time + ": " + str

        print(logStr)
        LOG_FILE.write(logStr + '\n')

        LOG_FILE.close()
