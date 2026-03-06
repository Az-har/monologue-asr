import logging
from pathlib import Path
from src.config.settings import LOG_DIR, LOG_FILE


def setup_logger():

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("pipeline")

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger