import logging
import os
from datetime import datetime

LOG_FILE = f"sensor_{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_PATH =  os.path.join("/Users/nikhil/Downloads","logs",LOG_FILE)
#print(LOG_PATH)
os.makedirs(LOG_PATH,exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_PATH, LOG_FILE)
#print(LOG_FILE_PATH)

logging.basicConfig(filename=LOG_FILE_PATH,format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",level=logging.INFO)