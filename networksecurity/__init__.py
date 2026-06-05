import os
import sys
import logging

LOG_FORMAT = "[%(asctime)s: %(levelname)s: %(name)s: %(module)s: %(message)s]"

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

log_filepath = os.path.join(log_dir, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(log_filepath, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
    force=True,  
)

logger = logging.getLogger("networksecurity")
