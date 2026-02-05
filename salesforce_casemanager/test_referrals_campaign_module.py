from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_referrals_sequence():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 30)

    list_views = [
        "All Referrals-Community",
        "Closed Cases",
        "No Report By Provider",
        "Recently Viewed Referrals",
        "Referrals - Unassigned"
    ]

    try:
        driver.get("https://opendoors--qa.sandbox.my.site.com/s/login/")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.input"))).send_keys(
            "udeme@opendoorsatl.org.qa.casemanager"
        )
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))).send_keys(
            "14Gconnect#1"
        )
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'loginButton')]"))).click()

        wait.until(EC.url_contains("/s/"))
        print("Login Successful")

        referrals_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Referrals & Campaign')]"))
        )
        referrals_tab.click()

        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(@class, 'slds-page-header__title') and contains(text(), 'Recently Viewed')]")
            )
        )
        print("Referrals page loaded")

        for view_name in list_views:
            dropdown_trigger = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@title, 'Select a List View')]"))
            )
            dropdown_trigger.click()

            view_item = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//span[normalize-space()='{view_name}']"))
            )
            view_item.click()
            print(f"Selected: {view_name}")

            header_xpath = f"//span[contains(@class, 'slds-page-header__title') and normalize-space()='{view_name}']"
            wait.until(EC.visibility_of_element_located((By.XPATH, header_xpath)))
            print(f"Verified: {view_name} header is visible")

            time.sleep(2)

        print("All list views verified successfully")

    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        driver.quit()
