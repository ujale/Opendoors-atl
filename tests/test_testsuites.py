from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def run_salesforce_report_suite():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 30)

    reports_to_test = [
        {"link": "Total Agency Referrals Submitted", "title": "Total Agency Referrals Submitted"},
        {"link": "Total Agency Housed", "title": "Total Agency Housed"},
        {"link": "Total Individuals Housed", "title": "Total Individuals Housed"},
        {"link": "Total Agency Open Referrals", "title": "Total Agency Open Referrals"},
        {"link": "Total Individual Open Referrals", "title": "Total Individual Open Referrals"}
        {"link": "Break Open Referrals down by status", "title": "Break Open Referrals down by status"}
    ]

    try:
        driver.get("https://opendoors--qa.sandbox.my.site.com/s/login/")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.input"))).send_keys("udeme@opendoorsatl.org.qa.casemanager")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))).send_keys("14Gconnect#1")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'loginButton')]"))).click()
        
        wait.until(EC.url_contains("/s/"))
        print("Login Successful")

        for report in reports_to_test:
            print(f"Testing: {report['link']}")

            dashboard_frame = wait.until(
                EC.presence_of_element_located((By.XPATH, "//iframe[contains(@title, 'dashboard')] | //iframe"))
            )
            driver.switch_to.frame(dashboard_frame)

            link_xpath = f"//a[contains(., '{report['link']}')]"
            report_link = wait.until(EC.element_to_be_clickable((By.XPATH, link_xpath)))
            driver.execute_script("arguments[0].click();", report_link)
            
            driver.switch_to.default_content()
            time.sleep(3)

            header_found = False
            header_xpath = f"//span[@title='{report['title']}']"

            try:
                wait.until(EC.visibility_of_element_located((By.XPATH, header_xpath)))
                header_found = True
            except:
                iframes = driver.find_elements(By.TAG_NAME, "iframe")
                for frame in iframes:
                    driver.switch_to.default_content()
                    driver.switch_to.frame(frame)
                    try:
                        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, header_xpath)))
                        header_found = True
                        break 
                    except:
                        continue
            
            if not header_found:
                raise Exception(f"Header not found: {report['title']}")

            print(f"Verified: {report['title']}")
            driver.switch_to.default_content()
            driver.back()
            time.sleep(4) 

        print("All reports verified successfully")

    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    run_salesforce_report_suite()