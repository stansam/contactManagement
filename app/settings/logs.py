import logging 
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

os.makedirs(LOG_DIR, exist_ok=True)

def init_logs():
    log_format = "[%(asctime)s] | [%(levelname)s] | [%(name)s] | line:%(lineno)d | %(message)s"

    logging.basicConfig(
        filename=LOG_FILE,
        filemode="a",  
        format=log_format,
        level=logging.DEBUG,
        encoding="utf-8"
    )