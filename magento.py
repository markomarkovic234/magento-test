from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep

def open_site(url):
    driver = webdriver.Chrome(service=Service(), options=webdriver.ChromeOptions())
    driver.maximize_window()
    driver.get(url)
    return driver

def close_browser(driver):
    driver.close()

def test_magento_smoke():
    driver = open_site('https://magento.softwaretestingboard.com/')
    sleep(2)
    assert "home" in driver.title.lower() or "page" in driver.title.lower(), "Title check failed"
    print('Home page title verified.')
    close_browser(driver)
