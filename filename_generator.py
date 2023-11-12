import os
from config import Config
from datetime import datetime


def generate(config: Config, action: str, ext: str):
    filename = datetime.now().strftime("%Y%m%d-%H%M%S.{ext}".format(ext=ext))
    return os.path.join(config.get_data_location(), action, filename)
