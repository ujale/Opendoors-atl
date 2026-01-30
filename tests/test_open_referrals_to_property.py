from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_open_referrals_to_property():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 45)

    try:
        driver.get("https://opendoors--qa.sandbox.my.site.com/s/login/")

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.input"))).send_keys("udeme@opendoorsatl.org.qa.casemanager")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))).send_keys("14Gconnect#1")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'loginButton')]"))).click()

        wait.until(EC.url_contains("/s/"))
        print("Login successful")

        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@title, 'dashboard')] | //iframe")))
        
        report_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Open Referrals To Property')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", report_link)
        time.sleep(2)
        driver.execute_script("arguments[0].click();", report_link)
        print("Clicked View Report")

        driver.switch_to.default_content()

        wait.until(EC.url_contains("00O3u0000078q26EAA"))
        wait.until(EC.presence_of_element_located((By.XPATH, "//tr[contains(@class, 'dataRow')] | //table//tbody//tr")))
        
        time.sleep(10)
        driver.execute_script("window.scrollTo(0, 500);")
        print("Report page fully loaded with data visible")

    except Exception as e:
        print(f"Error: {e}")
        driver.save_screenshot("report_loading_issue.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_open_referrals_to_property()