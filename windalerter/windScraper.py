from bs4 import BeautifulSoup

import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def get_webpage(url, wait_for_load: int=10):
    cap = DesiredCapabilities().CHROME
    cap["marionette"] = False
    browser = webdriver.Chrome(executable_path="C://Users/sjdll/chromedriver.exe")
    soup = None
    try:
        browser.get(url)
        time.sleep(wait_for_load)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
    finally:
        browser.close()
    return soup