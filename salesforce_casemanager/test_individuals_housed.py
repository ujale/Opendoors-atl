from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_agency_open_referrals():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 30)

    try:
        driver.get("https://opendoors--qa.sandbox.my.site.com/s/login/")

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.input"))).send_keys("udeme@opendoorsatl.org.qa.casemanager")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))).send_keys("14Gconnect#1")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'loginButton')]"))).click()

        wait.until(EC.url_contains("/s/"))
        print("Login successful")

        dashboard_frame = wait.until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@title, 'dashboard')] | //iframe"))
        )
        driver.switch_to.frame(dashboard_frame)

        referrals_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Total Agency Open Referrals')]"))
        )
        
        driver.execute_script("arguments[0].click();", referrals_link)
        print("Clicked View Report")

        driver.switch_to.default_content()
        
        wait.until(EC.url_contains("00OEa000003lUNVMA2"))
        
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, 500);")
        print("Report page loaded successfully")

    except Exception as e:
        print(f"Error: {e}")
        driver.switch_to.default_content()
        driver.save_screenshot("report_load_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_agency_open_referrals()