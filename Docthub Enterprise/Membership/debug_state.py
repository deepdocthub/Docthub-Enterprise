"""
Diagnostic: Navigate to Add Member form, select country = India,
then dump state field attributes and any visible dropdown options.
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
CHROMEDRIVER_PATH = r"C:\Users\DELL9\.wdm\drivers\chromedriver\win64\148.0.7778.97\chromedriver.exe"

LOGIN_URL = "https://enterprise.ibns.in/"
EMAIL    = "new.enterprise@yopmail.com"
PASSWORD = "Test@123"

def safe_click(driver, el):
    try: el.click()
    except: driver.execute_script("arguments[0].click();", el)

def main():
    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH))
    try:
        # Login
        driver.get(LOGIN_URL); driver.maximize_window(); time.sleep(2)
        if "login" not in driver.current_url.lower():
            try: driver.find_element(By.XPATH,"//a[contains(@href,'login')]").click(); time.sleep(2)
            except: pass
        WebDriverWait(driver,15).until(EC.presence_of_element_located((By.NAME,"email")))
        driver.find_element(By.NAME,"email").send_keys(EMAIL)
        driver.find_element(By.NAME,"password").send_keys(PASSWORD)
        driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
        time.sleep(4)

        # Navigate to Add Member form
        WebDriverWait(driver,15).until(EC.element_to_be_clickable(
            (By.XPATH,"/html/body/div[2]/div/div/main/div/div[3]/button[1]/div/div/p"))).click()
        time.sleep(3)
        WebDriverWait(driver,15).until(EC.element_to_be_clickable(
            (By.XPATH,"/html/body/div[2]/main/aside/aside/div/button[2]"))).click()
        time.sleep(3)
        WebDriverWait(driver,15).until(EC.element_to_be_clickable(
            (By.XPATH,"/html/body/div[2]/header/div/div[2]/div[2]/button"))).click()
        time.sleep(4)
        print("Add Member form open.")

        # Select Country = India
        country_el = driver.find_element(By.XPATH,"(//input[@placeholder='Select Country'])[1]")
        safe_click(driver, country_el)
        driver.execute_script("arguments[0].value = '';", country_el)
        country_el.send_keys("India")
        time.sleep(3)

        opt_xpath = "//*[@role='option'] | //div[contains(@class,'option')] | //li[contains(@class,'option')]"
        opts = [o for o in driver.find_elements(By.XPATH, opt_xpath) if o.is_displayed()]
        print(f"\nCountry options found: {len(opts)}")
        for o in opts[:5]:
            print(f"  '{o.text}'")

        if opts:
            # Click the India option
            for o in opts:
                if "india" in o.text.lower():
                    safe_click(driver, o)
                    print(f"Clicked: '{o.text}'")
                    break
        time.sleep(3)

        # Now inspect State field
        print("\n--- STATE FIELD AFTER COUNTRY SELECTION ---")
        state_el = driver.find_element(By.XPATH,"(//input[@placeholder='Select State'])[1]")
        print(f"  tag:         {state_el.tag_name}")
        print(f"  type:        {state_el.get_attribute('type')}")
        print(f"  value:       {state_el.get_attribute('value')}")
        print(f"  disabled:    {state_el.get_attribute('disabled')}")
        print(f"  readonly:    {state_el.get_attribute('readonly')}")
        print(f"  class:       {state_el.get_attribute('class')[:80]}")
        print(f"  visible:     {state_el.is_displayed()}")
        print(f"  enabled:     {state_el.is_enabled()}")

        # Try clicking state and see what happens
        print("\nClicking state field...")
        safe_click(driver, state_el)
        time.sleep(2)

        state_opts = [o for o in driver.find_elements(By.XPATH, opt_xpath) if o.is_displayed()]
        print(f"Options after click: {len(state_opts)}")

        # Try typing
        print("Typing 'a'...")
        state_el.send_keys("a")
        time.sleep(2)
        state_opts2 = [o for o in driver.find_elements(By.XPATH, opt_xpath) if o.is_displayed()]
        print(f"Options after typing 'a': {len(state_opts2)}")
        for o in state_opts2[:5]:
            print(f"  '{o.text}'")

        # Dump parent structure of state field
        print("\n--- STATE FIELD PARENT HTML ---")
        parent = driver.execute_script("return arguments[0].parentElement.outerHTML;", state_el)
        print(parent[:800])

    except Exception as e:
        import traceback; traceback.print_exc()
    finally:
        input("\nPress Enter to close...")
        driver.quit()

if __name__ == "__main__":
    main()
