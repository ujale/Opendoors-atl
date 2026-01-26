from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.maximize_window()
# 50 seconds is quite long; usually 20-30 is the "sweet spot" 
# to prevent the HTTP timeout error you saw earlier.
wait = WebDriverWait(driver, 20) 

try:
    # ---------- LOGIN ----------
    driver.get("https://opendoors--qa.sandbox.my.site.com/s/login/")

    username = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.input")))
    username.send_keys("udeme@opendoorsatl.org.qa.casemanager")

    password = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
    password.send_keys("14Gconnect#1")

    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'loginButton')]")))
    login_btn.click()

    wait.until(EC.url_contains("/s/"))
    print("✅ Login successful")

    # ---------- OPEN PROFILE MENU ----------
    # 1. Wait until the element is actually visible to the user
    print("🔄 Waiting for profile button visibility...")
    profile_btn = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "profile-menuTrigger"))
    )
    
    
    
    # 3. Finally, click it
    profile_btn.click()
    print("✅ Profile menu opened")

    # ---------- LOGOUT ----------
    # Apply the same logic for the logout button
    logout_btn = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".profile-menuItem.logOut.uiMenuItem"))
    )
    logout_btn.click()

    wait.until(EC.url_contains("/login"))
    print("✅ Logout successful")
    
    # ---------- VERIFY LOGIN PAGE REAPPEARANCE ----------
    # We look for the login button class you provided to confirm we are back
    # This confirms the logout was successful and the login page has re-rendered
    login_page_marker = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".slds-button.slds-button--brand.loginButton.uiButton--none.uiButton")
        )
    )
    
    if login_page_marker.is_displayed():
        print("✅ Logout verified: Login button is visible again.")
except Exception as e:
    print(f"❌ Test failed: {e}")
    driver.save_screenshot("logout_failure.png")
    raise

   
finally:
    driver.quit()