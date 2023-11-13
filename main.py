#!/usr/bin/env python3
import datetime
import os.path
import graph_data_manager
from config import Config
from screenshot import save_screenshot
from page_reader import PageReader
import os

DEFAULT_DATE_FORMAT = "%Y%m%d %H%M"


def prep_directories(config: Config):
    data_location = config.get_data_location()
    if not os.path.exists(data_location):
        os.mkdir(data_location)
        os.mkdir(os.path.join(data_location, "screenshot"))
        os.mkdir(os.path.join(data_location, "snapshot"))
        os.mkdir(os.path.join(data_location, "csv"))


def update_local_date(date: datetime.datetime, config: Config):
    with open(config.get_last_updated_file(), 'w') as f:
        f.write(date.strftime(DEFAULT_DATE_FORMAT))
        f.flush()


def read_local_date(config: Config):
    if os.path.exists(config.get_last_updated_file()):
        with open(config.get_last_updated_file(), 'r') as f:
            txt = f.read()
            return datetime.datetime.strptime(txt, DEFAULT_DATE_FORMAT)

    else:
        return None


def main():
    config = Config()
    prep_directories(config)
    reader = PageReader(config)

    page_last_update = reader.get_last_update()
    local_update = read_local_date(config)

    if local_update is None or page_last_update > local_update:
        save_screenshot(config)

        reader.snapshot_page()

        graphs = reader.fetch_graphs()
        graph_data_manager.write_to_file(config, graphs)

        update_local_date(page_last_update, config)


if __name__ == '__main__':
    main()
