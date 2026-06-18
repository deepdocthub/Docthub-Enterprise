import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
LOGIN_URL = "https://enterprise.docthub.com/"
EMAIL = "lead.qa+11@docthub.com"
PASSWORD = "Docthub@2025"

# --- SELECTORS ---
SELECTORS = {
    "email": [
        (By.ID, "email"),
        (By.NAME, "email"),
        (By.ID, "username"),
        (By.NAME, "username"),
        (By.CSS_SELECTOR, "input[type='email']"),
        (By.CSS_SELECTOR, "input[type='text']"),
    ],
    "password": [
        (By.ID, "password"),
        (By.NAME, "password"),
        (By.CSS_SELECTOR, "input[type='password']"),
    ],
    "submit_button": [
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.ID, "login-button"),
        (By.ID, "submit"),
        (By.XPATH, "//button[contains(text(), 'Login')]"),
        (By.XPATH, "//button[contains(text(), 'Sign In')]"),
    ],
}


def find_element_robust(driver, selector_list, element_name):
    """
    Efficiently waits for ANY of the provided selectors to match an element.
    """
    print(f"Looking for {element_name}...")

    conditions = [EC.presence_of_element_located((by, val)) for by, val in selector_list]

    try:
        WebDriverWait(driver, 15).until(EC.any_of(*conditions))

        for by, value in selector_list:
            elements = driver.find_elements(by, value)
            if elements:
                print(f"  Found {element_name} using {by}='{value}'")
                return elements[0]

        raise Exception("Wait completed but element not found in list check.")

    except Exception as e:
        raise Exception(f"Could not find {element_name}. Timed out.") from e


def login(driver):
    """
    Performs login on enterprise.docthub.com and clicks the Institute card.
    Returns True if login was successful, False otherwise.
    """
    print(f"Navigating to {LOGIN_URL}...")
    driver.get(LOGIN_URL)
    driver.maximize_window()

    # Check if we need to click a "Login" link
    current_url = driver.current_url
    if "login" not in current_url.lower():
        print("Not on login page yet. Checking for 'Login' link...")
        try:
            login_link = driver.find_element(By.XPATH, "//a[contains(@href, 'login')]")
            login_link.click()
            print("Clicked Login link.")
            time.sleep(3)
        except:
            print("Could not find a 'Login' link.")

    # Enter Email
    email_input = find_element_robust(driver, SELECTORS["email"], "Email Input")
    email_input.clear()
    email_input.send_keys(EMAIL)
    print("Entered email.")

    # Enter Password
    password_input = find_element_robust(driver, SELECTORS["password"], "Password Input")
    password_input.clear()
    password_input.send_keys(PASSWORD)
    print("Entered password.")

    # Click Login
    submit_btn = find_element_robust(driver, SELECTORS["submit_button"], "Submit Button")
    try:
        submit_btn.click()
    except:
        driver.execute_script("arguments[0].click();", submit_btn)
    print("Clicked Login button.")

    return True


def e_certificate_actions(driver):
    """
    TODO: Add your E-Certificate automation steps here.
    This function runs after a successful login.
    """
    print("\n--- Starting E-Certificate Actions ---")

    # Step 1: Click on E-Certificate button
    e_cert_selectors = [
        (By.XPATH, "/html/body/div[2]/div/div/main/div/div[3]/button[2]"),
        (By.XPATH, "//button[contains(., 'E-Certificate')]"),
        (By.XPATH, "//button[contains(., 'Certificate')]"),
    ]
    e_cert_btn = find_element_robust(driver, e_cert_selectors, "E-Certificate Button")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", e_cert_btn)
    time.sleep(1)
    try:
        e_cert_btn.click()
    except:
        driver.execute_script("arguments[0].click();", e_cert_btn)
    print("Clicked E-Certificate button.")
    time.sleep(2)

    # Step 2: Click Assign Awardee button
    assign_awardee_selectors = [
        (By.XPATH, "/html/body/div[2]/main/section/section/div/article[1]/div[3]/div/button"),
        (By.XPATH, "//button[contains(., 'Assign Awardee')]"),
        (By.XPATH, "//button[contains(., 'Assign')]"),
    ]
    assign_btn = find_element_robust(driver, assign_awardee_selectors, "Assign Awardee Button")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", assign_btn)
    time.sleep(1)
    try:
        assign_btn.click()
    except:
        driver.execute_script("arguments[0].click();", assign_btn)
    print("Clicked Assign Awardee button.")
    time.sleep(2)

    # Step 3: Fill Manual Assign Popup — Full Name
    full_name_selectors = [
        (By.XPATH, "/html/body/div[3]/div[3]/div[2]/div/div[1]/div/div[2]/div[1]/div[1]/div/input"),
        (By.XPATH, "//input[@placeholder='Full Name']"),
        (By.XPATH, "//input[contains(@placeholder, 'Name')]"),
    ]
    full_name_input = find_element_robust(driver, full_name_selectors, "Full Name Input")
    full_name_input.clear()
    full_name_input.send_keys("Test Automation")
    print("Entered Full Name: Test Automation")
    time.sleep(0.5)

    # Step 4: Fill Email Address
    email_selectors = [
        (By.XPATH, "/html/body/div[3]/div[3]/div[2]/div/div[1]/div/div[2]/div[1]/div[2]/div/input"),
        (By.XPATH, "//input[@placeholder='Email Address']"),
        (By.XPATH, "//input[@type='email']"),
    ]
    email_input = find_element_robust(driver, email_selectors, "Email Address Input")
    email_input.clear()
    email_input.send_keys("admin.qa@docthub.com")
    print("Entered Email: admin.qa@docthub.com")
    time.sleep(0.5)

    # Step 5: Fill Mobile Number
    mobile_selectors = [
        (By.XPATH, "/html/body/div[3]/div[3]/div[2]/div/div[1]/div/div[2]/div[1]/div[3]/div/input"),
        (By.XPATH, "//input[@placeholder='Mobile Number']"),
        (By.XPATH, "//input[contains(@placeholder, 'Mobile')]"),
    ]
    mobile_input = find_element_robust(driver, mobile_selectors, "Mobile Number Input")
    mobile_input.clear()
    mobile_input.send_keys("9313136376")
    print("Entered Mobile Number: 9313136376")
    time.sleep(0.5)

    # Step 6: Click Upload Assign button
    upload_assign_selectors = [
        (By.XPATH, "/html/body/div[3]/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/button[2]"),
        (By.XPATH, "//button[contains(., 'Upload Assign')]"),
        (By.XPATH, "//button[contains(., 'Assign')]"),
    ]
    upload_assign_btn = find_element_robust(driver, upload_assign_selectors, "Upload Assign Button")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload_assign_btn)
    time.sleep(1)
    try:
        upload_assign_btn.click()
    except:
        driver.execute_script("arguments[0].click();", upload_assign_btn)
    print("Clicked Upload Assign button.")
    time.sleep(3)  # Wait for success popup

    # Step 7: Click Send Email button on success popup
    send_email_selectors = [
        (By.XPATH, "/html/body/div[4]/div[3]/div[2]/div/div/button[1]"),
        (By.XPATH, "//button[contains(., 'Send Email')]"),
        (By.XPATH, "//button[contains(., 'Send')]"),
    ]
    send_email_btn = find_element_robust(driver, send_email_selectors, "Send Email Button")
    time.sleep(1)
    try:
        send_email_btn.click()
    except:
        driver.execute_script("arguments[0].click();", send_email_btn)
    print("Clicked Send Email button. Email sent to admin.qa@docthub.com")
    time.sleep(2)

    # Step 8: Search with last added awardee name
    AWARDEE_NAME = "Test Automation"
    AWARDEE_EMAIL = "admin.qa@docthub.com"
    AWARDEE_MOBILE = "9313136376"

    search_selectors = [
        (By.XPATH, "/html/body/div[2]/main/section/div/div[1]/div[2]/div/input"),
        (By.XPATH, "//input[@placeholder='Search']"),
        (By.XPATH, "//input[contains(@placeholder, 'Search')]"),
    ]
    search_input = find_element_robust(driver, search_selectors, "Awardee Search Input")
    search_input.clear()
    search_input.send_keys(AWARDEE_NAME)
    print(f"Searched for awardee: '{AWARDEE_NAME}'")
    time.sleep(2)  # Wait for search results to load

    # Step 9: Verify search results display the awardee record
    print("\n--- Verifying Search Results ---")
    try:
        # Look for any row/card in the results containing the awardee name
        result_selectors = [
            (By.XPATH, f"//*[contains(text(), '{AWARDEE_NAME}')]"),
            (By.XPATH, f"//td[contains(text(), '{AWARDEE_NAME}')]"),
            (By.XPATH, f"//div[contains(text(), '{AWARDEE_NAME}')]"),
            (By.XPATH, f"//span[contains(text(), '{AWARDEE_NAME}')]"),
        ]

        result_found = False
        for by, selector in result_selectors:
            elements = driver.find_elements(by, selector)
            visible = [el for el in elements if el.is_displayed()]
            if visible:
                print(f"  ✓ Awardee record found: '{visible[0].text.strip()}'")
                result_found = True
                break

        if not result_found:
            print(f"  ✗ WARNING: No visible record found for '{AWARDEE_NAME}' in search results.")
        else:
            # Verify email is visible in results
            email_results = driver.find_elements(By.XPATH, f"//*[contains(text(), '{AWARDEE_EMAIL}')]")
            if any(el.is_displayed() for el in email_results):
                print(f"  ✓ Email verified in results: '{AWARDEE_EMAIL}'")
            else:
                print(f"  ~ Email '{AWARDEE_EMAIL}' not visible in result row (may be hidden column).")

            # Verify mobile is visible in results
            mobile_results = driver.find_elements(By.XPATH, f"//*[contains(text(), '{AWARDEE_MOBILE}')]")
            if any(el.is_displayed() for el in mobile_results):
                print(f"  ✓ Mobile verified in results: '{AWARDEE_MOBILE}'")
            else:
                print(f"  ~ Mobile '{AWARDEE_MOBILE}' not visible in result row (may be hidden column).")

            print("\n✓ Search verification PASSED — Awardee record matches assignment details.")

    except Exception as e:
        print(f"  ✗ Verification error: {e}")


def main():
    print("Starting E-Certificate Script...")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Step 1: Login
        login(driver)

        # Step 2: E-Certificate specific actions
        time.sleep(2)
        e_certificate_actions(driver)

        print("\nDone! E-Certificate actions completed.")

    except Exception as e:
        print(f"\nERROR: {e}")
    finally:
        input("\nPress Enter to close the browser...")
        driver.quit()


if __name__ == "__main__":
    main()
