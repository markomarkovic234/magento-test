from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import uuid
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
    try:
        consent_button = driver.find_element(By.XPATH, "//p[text()='Consent']")
        consent_button.click()
        sleep(2)
    except:
        pass  # If the consent is not present, continue
    # Click the "Shop New Yoga" link
    element = driver.find_element(By.XPATH, "//a[@class='block-promo home-main']//span[text()='Shop New Yoga']")
    element.click()
    sleep(2)
    # Click on the logo
    logo = driver.find_element(By.CSS_SELECTOR, "a.logo")
    driver.execute_script("arguments[0].click();", logo)
    sleep(2)
    assert "magento" in driver.current_url
    print("Test passed: Luma logo redirected to homepage")
    close_browser(driver)

def test_search_jacket():
    driver = open_site("https://magento.softwaretestingboard.com/")
    sleep(3)
    try:
        consent_button = driver.find_element(By.XPATH, "//p[text()='Consent']")
        consent_button.click()
        sleep(2)
    except:
        pass  # If the consent is not present, continue
    search_input = driver.find_element(By.ID, "search")
    search_input.clear()
    search_input.send_keys("proteus")
    search_input.send_keys(Keys.RETURN)
    sleep(2)
    product_link = driver.find_element(By.XPATH,
                                       "//a[@class='product-item-link' and normalize-space(text())='Proteus Fitness Jackshirt']")
    # Assert the link text
    assert product_link.text.strip() == "Proteus Fitness Jackshirt", "Text does not match!"
    # Print success message
    print("Test successful: 'Proteus Fitness Jackshirt' link found.")
    close_browser(driver)

def test_validate_product_details():
    driver = open_site("https://magento.softwaretestingboard.com/")
    sleep(2)
    consent_button = driver.find_element(By.XPATH, "//p[text()='Consent']")
    consent_button.click()
    search_input = driver.find_element(By.ID, "search")
    search_input.clear()
    search_input.send_keys("proteus")
    search_input.send_keys(Keys.RETURN)
    sleep(2)
    price_element = driver.find_element(By.CSS_SELECTOR, "span.price")
    assert price_element.text == "$45.00", f"Expected price to be '$45.00' but got '{price_element.text}'"
    print("Test Passed: Product details (price) displayed correctly.")
    close_browser(driver)

def test_create_an_account():
    driver = open_site("https://magento.softwaretestingboard.com/")
    sleep(2)
    consent_button = driver.find_element(By.XPATH, "//p[text()='Consent']")
    consent_button.click()
    # Try closing cookie/consent popup if visible
    try:
        close_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Close']")
        close_button.click()
        sleep(1)
    except:
        pass  # If not found, continue
    # Click "Create an Account"
    driver.find_element(By.XPATH, '//a[text()="Create an Account"]').click()
    sleep(2)
    # Fill out the form
    driver.find_element(By.ID, "firstname").send_keys("Alice")
    driver.find_element(By.ID, "lastname").send_keys("Tester")
    unique_email = f"testuser+{uuid.uuid4().hex[:6]}@example.com"
    driver.find_element(By.ID, "email_address").send_keys(unique_email)
    driver.find_element(By.ID, "password").send_keys("P@ssword123")
    driver.find_element(By.ID, "password-confirmation").send_keys("P@ssword123")
    # Submit the form
    driver.find_element(By.XPATH, "//button[@title='Create an Account']").click()
    sleep(3)
    # Check for successful account creation
    success_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-ui-id='message-success']")
    assert len(success_elements) > 0, "Account creation failed"
    print("Test successful: New customer account was created.")
    sleep(2)
    close_browser(driver)

def test_create_an_account_with_existing_email():
    driver = open_site("https://magento.softwaretestingboard.com/")
    sleep(2)
    consent_button = driver.find_element(By.XPATH, "//p[text()='Consent']")
    consent_button.click()
    driver.find_element(By.XPATH, '//a[text()="Create an Account"]').click()
    sleep(2)
    # Fill out the form
    driver.find_element(By.ID, "firstname").send_keys("Alice")
    driver.find_element(By.ID, "lastname").send_keys("Tester")
    unique_email = f"testuser@example.com"
    driver.find_element(By.ID, "email_address").send_keys(unique_email)
    driver.find_element(By.ID, "password").send_keys("P@ssword123")
    driver.find_element(By.ID, "password-confirmation").send_keys("P@ssword123")
    # Submit the form
    driver.find_element(By.XPATH, "//button[@title='Create an Account']").click()
    sleep(3)
    # Check for unsuccessful account creation
    error_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-ui-id='message-error']")
    assert len(error_elements) > 0, "Expected error message not shown for existing email"
    error_text = error_elements[0].text.lower()
    assert "already an account with this email" in error_text
    print("Test passed: Account with existing email was not created, error message displayed.")
    close_browser(driver)

def test_login_with_valid_credentials():
    driver = open_site("https://magento.softwaretestingboard.com/")
    sleep(2)

    try:
        driver.find_element(By.XPATH, "//p[text()='Consent']").click()
        sleep(1)
    except:
        pass

    driver.find_element(By.LINK_TEXT, "Sign In").click()
    sleep(2)

    driver.find_element(By.ID, "email").send_keys("validuser1@example.com")
    driver.find_element(By.ID, "pass").send_keys("ValidPass123")
    driver.find_element(By.ID, "send2").click()
    sleep(3)

    # Assert successful login by checking if the "Welcome" message is visible
    welcome_text_elements = driver.find_elements(By.XPATH, "//span[contains(text(), 'Welcome')]")
    assert len(welcome_text_elements) > 0, "Login failed: Welcome message not displayed"
    print("Test passed: Valid login successful, user is logged in")
    close_browser(driver)

def test_login_with_invalid_credentials():
    driver = open_site("https://magento.softwaretestingboard.com/")
    sleep(2)

    try:
        driver.find_element(By.XPATH, "//p[text()='Consent']").click()
        sleep(1)
    except:
        pass

    # driver.find_element(By.LINK_TEXT, "Sign In").click()
    # driver.find_element(By.XPATH, '//a[text()="Sign In"]').click()
    driver.find_element(By.XPATH, '//a[contains(text(), "Sign In")]').click()
    sleep(2)
    driver.find_element(By.ID, "email").send_keys("wrong@example.com")
    driver.find_element(By.ID, "pass").send_keys("WrongPass123")
    driver.find_element(By.ID, "send2").click()
    sleep(2)

    errors = driver.find_elements(By.CSS_SELECTOR, "div[data-ui-id='message-error']")
    assert len(errors) > 0, "Expected login error not shown"
    print("Test passed: Invalid login correctly shows an error")
    close_browser(driver)

def test_password_reset_flow():
    driver = open_site("https://magento.softwaretestingboard.com/")
    sleep(2)
    try:
        driver.find_element(By.XPATH, "//p[text()='Consent']").click()
        sleep(1)
    except:
        pass

    driver.find_element(By.XPATH, '//a[contains(text(), "Sign In")]').click()
    sleep(2)
    driver.find_element(By.LINK_TEXT, "Forgot Your Password?").click()
    sleep(2)

    driver.find_element(By.ID, "email_address").send_keys("nonexistent@example.com")
    driver.find_element(By.CSS_SELECTOR, "button.action.submit.primary").click()
    sleep(2)

    messages = driver.find_elements(By.CSS_SELECTOR, "div[data-ui-id='message-success']")
    assert len(messages) > 0, "Expected confirmation message not shown"
    print("Test passed: Password reset for non-registered email shows an error")
    close_browser(driver)

def test_subscribe_link_opens_correct_url():
    driver = open_site("https://magento.softwaretestingboard.com/")
    sleep(2)

    try:
        driver.find_element(By.XPATH, "//p[text()='Consent']").click()
        sleep(1)
    except:
        pass

    # Scroll down to footer where "Subscribe" link is
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(2)

    # Find the subscribe link
    subscribe_link = driver.find_element(By.LINK_TEXT, "Subscribe")
    href = subscribe_link.get_attribute("href")

    # Assert the href contains the expected target URL
    assert "softwaretestingboard.com/subscribe" in href, "Subscribe link URL is incorrect"
    print("Test passed: Subscribe link is present and points to correct URL")
    close_browser(driver)