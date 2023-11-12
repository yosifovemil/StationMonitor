#!/usr/bin/env python3
import configparser
from screenshot import save_screenshot

config = configparser.ConfigParser()
config.read('settings.ini')
target_url = config['TARGET']['URL'].strip()
save_screenshot(target_url)
