from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_dashboard():
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

        wait.until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Home']")))
        print("Dashboard loaded")

        # --- SWITCH TO DASHBOARD IFRAME ---
        dashboard_frame = wait.until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@title, 'dashboard')] | //iframe"))
        )
        driver.switch_to.frame(dashboard_frame)
        print("Switched to dashboard iframe")

        # --- CLICK VIEW REPORT ---
        view_report_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'View Report')]"))
        )
        driver.execute_script("arguments[0].click();", view_report_link)
        print("Clicked View Report")

        # --- VALIDATE REPORT PAGE ---
        driver.switch_to.default_content()
        wait.until(EC.url_contains("00OEa000003lU8zMAE"))
        
        
        import time
        time.sleep(5) 
        
        driver.save_screenshot("agency_referrals_report.png")
        print("Report page loaded and screenshot saved")

        driver.back()

    except Exception as e:
        print(f"Test failed: {e}")
        driver.save_screenshot("dashboard_failure.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_dashboard()