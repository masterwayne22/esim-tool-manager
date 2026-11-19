import logging
from pathlib import Path

LOG_DIR = Path.home() / ".esim"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "manager.log"

def setup_logger():
    logger = logging.getLogger("esim_manager")
    logger.setLevel(logging.DEBUG)
    
    # Avoid duplicate handlers
    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger

logger = setup_logger()