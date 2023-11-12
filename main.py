#!/usr/bin/env python3
import os.path

import graph_data_manager
from config import Config
from screenshot import save_screenshot
from page_reader import PageReader
import os


def prep_directories(config: Config):
    data_location = config.get_data_location()
    if not os.path.exists(data_location):
        os.mkdir(data_location)
        os.mkdir(os.path.join(data_location, "screenshot"))
        os.mkdir(os.path.join(data_location, "snapshot"))
        os.mkdir(os.path.join(data_location, "csv"))


def main():
    config = Config()
    prep_directories(config)

    save_screenshot(config)

    reader = PageReader(config)
    reader.snapshot_page()

    graphs = reader.fetch_graphs()
    graph_data_manager.write_to_file(config, graphs)


if __name__ == '__main__':
    main()
