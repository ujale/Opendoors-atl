import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_referrals_search(driver):
    wait = WebDriverWait(driver, 60)

    driver.get("https://opendoors--qa.sandbox.my.site.com/s/login/")

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.input"))).send_keys("udeme@opendoorsatl.org.qa.casemanager")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))).send_keys("14Gconnect#1")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'loginButton')]"))).click()

    assert wait.until(EC.url_contains("/s/")), "Login failed"

    referrals_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Referrals & Campaign')]")))
    referrals_tab.click()

    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Recently Viewed')]")))

    search_query = "Uti Uti"

    find_script = """
    function findInShadow(selector, root = document) {
        let el = root.querySelector(selector);
        if (el) return el;
        for (let node of root.querySelectorAll('*')) {
            if (node.shadowRoot) {
                let found = findInShadow(selector, node.shadowRoot);
                if (found) return found;
            }
        }
        return null;
    }
    return findInShadow('input[name="Case-search-input"]');
    """

    search_input = wait.until(lambda d: d.execute_script(find_script))
    search_input.click()
    search_input.send_keys(Keys.CONTROL + "a")
    search_input.send_keys(Keys.DELETE)
    search_input.send_keys(search_query)
    search_input.send_keys(Keys.ENTER)

    time.sleep(10)

    result_xpath = f"//table//tbody//tr//a[contains(., '{search_query}')] | //table//tbody//tr//span[contains(., '{search_query}')]"
    
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, result_xpath)))
    except:
        pytest.fail(f"Search results for '{search_query}' did not appear in the table.")

    rows = driver.find_elements(By.XPATH, "//table//tbody//tr")
    assert len(rows) >= 1