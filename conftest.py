import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def login(driver):
    wait = WebDriverWait(driver, 30)

    driver.get("https://opendoors--qa.sandbox.my.site.com/s/login/")

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input.input"))
    ).send_keys("udeme@opendoorsatl.org.qa.casemanager")

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@type='password']"))
    ).send_keys("14Gconnect#1")

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class,'loginButton')]"))
    ).click()

    wait.until(EC.url_contains("/s/"))
