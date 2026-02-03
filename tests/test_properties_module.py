import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

LIST_VIEWS = [
    "All Live Properties",
    "All Properties",
    "Recently Viewed"
]

def test_properties_list(driver):
    wait = WebDriverWait(driver, 30)

    driver.get("https://opendoors--qa.sandbox.my.site.com/s/login/")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.input"))).send_keys("udeme@opendoorsatl.org.qa.casemanager")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))).send_keys("14Gconnect#1")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'loginButton')]"))).click()
    
    assert wait.until(EC.url_contains("/s/"))

    properties_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Properties')]")))
    properties_tab.click()

    for view_name in LIST_VIEWS:
        dropdown_trigger = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@title, 'Select a List View')]")))
        driver.execute_script("arguments[0].click();", dropdown_trigger)
        
        view_item_xpath = f"//span[normalize-space()='{view_name}']"
        item = wait.until(EC.presence_of_element_located((By.XPATH, view_item_xpath)))
        driver.execute_script("arguments[0].click();", item)

        header_xpath = f"//span[contains(@class, 'slds-page-header__title') and normalize-space()='{view_name}']"
        header_visible = wait.until(EC.visibility_of_element_located((By.XPATH, header_xpath)))
        
        assert header_visible.is_displayed()
        time.sleep(2)