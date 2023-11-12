from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
from config import Config
import filename_generator


def save_screenshot(config: Config):
    op = Options()
    op.add_argument("--headless")
    op.add_argument("--disable-gpu")

    filename = filename_generator.generate(config, "screenshot", "png")

    # display = Display(visible=False, size=(800, 600))
    # display.start()

    driver = webdriver.Chrome(options=op)
    driver.get(config.get_url())
    take_screenshot(driver, filename)
    driver.quit()

    # display.stop()


def take_screenshot(driver: webdriver.Chrome, path: str) -> None:
    # Ref: https://stackoverflow.com/a/52572919/
    original_size = driver.get_window_size()
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    driver.find_element(By.TAG_NAME, 'body').screenshot(path)  # avoids scrollbar
    driver.set_window_size(original_size['width'], original_size['height'])
