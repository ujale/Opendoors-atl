from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_dashboard():
    # ---------------- SETUP ----------------
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 30)

    try:
        # ---------------- LOGIN ----------------
        driver.get("https://opendoors--qa.sandbox.my.site.com/s/login/")

        username = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.input"))
        )
        username.send_keys("udeme@opendoorsatl.org.qa.casemanager")

        password = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))
        )
        password.send_keys("14Gconnect#1")

        login_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class,'loginButton')]")
            )
        )
        login_btn.click()

        wait.until(EC.url_contains("/s/"))
        print("Login successful")

        # ---------------- DASHBOARD VALIDATION ----------------
        home_tab = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//a[normalize-space()='Home']")
            )
        )
        assert home_tab.is_displayed()
        print("Dashboard loaded (Home tab visible)")


    except Exception as e:
        print(f"Test failed: {e}")
        driver.save_screenshot("dashboard_failure.png")
        raise

    finally:
        driver.quit()


if __name__ == "__main__":
    test_dashboard()
