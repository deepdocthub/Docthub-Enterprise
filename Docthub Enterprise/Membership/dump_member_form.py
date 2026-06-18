"""
Diagnostic: logs in → Membership Management → Members Directory → Add New Member,
then dumps every input/textarea/select/button with its attributes.
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

LOGIN_URL = "https://enterprise.ibns.in/"
EMAIL    = "new.enterprise@yopmail.com"
PASSWORD = "Test@123"

def wait_click(driver, by, val, label, timeout=15):
    print(f"Clicking: {label}...")
    el = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, val)))
    try:
        el.click()
    except Exception:
        driver.execute_script("arguments[0].click();", el)
    print(f"  OK: {label}")
    return el

def dump_fields(driver):
    print("\n" + "="*70)
    print("  ALL FORM FIELDS IN ADD NEW MEMBER FORM")
    print("="*70)
    for tag in ["input", "textarea", "select"]:
        elements = driver.find_elements(By.TAG_NAME, tag)
        for el in elements:
            try:
                print({
                    "tag":         tag,
                    "type":        el.get_attribute("type") or "",
                    "id":          el.get_attribute("id") or "",
                    "name":        el.get_attribute("name") or "",
                    "placeholder": el.get_attribute("placeholder") or "",
                    "aria-label":  el.get_attribute("aria-label") or "",
                    "role":        el.get_attribute("role") or "",
                    "value":       el.get_attribute("value") or "",
                    "visible":     el.is_displayed(),
                })
            except Exception as e:
                print(f"  Error: {e}")

    print("\n  --- BUTTONS ---")
    for btn in driver.find_elements(By.TAG_NAME, "button"):
        try:
            print({
                "text":    btn.text.strip()[:80],
                "type":    btn.get_attribute("type") or "",
                "id":      btn.get_attribute("id") or "",
                "role":    btn.get_attribute("role") or "",
                "aria-label": btn.get_attribute("aria-label") or "",
                "visible": btn.is_displayed(),
            })
        except Exception as e:
            print(f"  Error: {e}")

def main():
    service = Service(ChromeDriverManager().install())
    driver  = webdriver.Chrome(service=service)

    try:
        # --- Login ---
        print("Navigating to site...")
        driver.get(LOGIN_URL)
        driver.maximize_window()
        time.sleep(2)

        if "login" not in driver.current_url.lower():
            try:
                driver.find_element(By.XPATH, "//a[contains(@href,'login')]").click()
                time.sleep(2)
            except:
                pass

        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "email")))
        driver.find_element(By.NAME, "email").send_keys(EMAIL)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(4)
        print("Logged in. URL:", driver.current_url)

        # --- Membership Management ---
        wait_click(driver,
            By.XPATH, "/html/body/div[2]/div/div/main/div/div[3]/button[1]/div/div/p",
            "Membership Management")
        time.sleep(3)

        # --- Members Directory sidebar button ---
        wait_click(driver,
            By.XPATH, "/html/body/div[2]/main/aside/aside/div/button[2]",
            "Members Directory")
        time.sleep(3)
        print("Members Directory URL:", driver.current_url)

        # --- New Member button ---
        wait_click(driver,
            By.XPATH, "/html/body/div[2]/header/div/div[2]/div[2]/button",
            "New Member Button")
        time.sleep(4)
        print("Add New Member form opened.")

        # --- Dump ---
        dump_fields(driver)

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback; traceback.print_exc()
    finally:
        input("\nPress Enter to close browser...")
        driver.quit()

if __name__ == "__main__":
    main()
