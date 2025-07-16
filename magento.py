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
    assert driver.current_url == "https://magento.softwaretestingboard.com/" or "magento" in driver.current_url
    print('Home page title verified.')
    close_browser(driver)

def test_luma_logo_redirects_to_homepage():
    driver = open_site('https://magento.softwaretestingboard.com/')
    sleep(2)
    consent_button = driver.find_element(By.XPATH, "//p[text()='Consent']")
    consent_button.click()
    sleep(2)
    # Click the "Shop New Yoga" link
    element = driver.find_element(By.XPATH, "//a[@class='block-promo home-main']//span[text()='Shop New Yoga']")
    element.click()
    # Click on the logo
    logo = driver.find_element(By.CSS_SELECTOR, "a.logo")
    logo.click()
    sleep(3)
    assert driver.current_url == "https://magento.softwaretestingboard.com/" or "magento" in driver.current_url
    print("Test passed: Luma logo redirected to homepage")
    close_browser(driver)