import os
import logging

_ICON_FOLDER = 'icons'


def setup_logger(logging_level: int):
    logger = logging.getLogger("image_converter")

    if not logger.hasHandlers():
        logger.setLevel(logging_level)

        ch = logging.StreamHandler()
        ch.setLevel(logging_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger


def get_icon_path(icon_name):
    return os.path.join('src', 'image_converter', 'resources', _ICON_FOLDER, icon_name)
